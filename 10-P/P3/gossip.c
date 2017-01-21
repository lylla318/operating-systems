#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "global.h"

struct gossip {
    struct gossip *next;
    struct sockaddr_in src;
    long counter; 
    char *latest;
};
static struct gossip *gossip;

struct node* all = NULL;
struct node* first = NULL;
struct node* last = NULL;

int node_no = 0;

extern struct sockaddr_in my_addr;

struct gossip* gossip_next(struct gossip* gossip) {
    return gossip->next;
}

struct sockaddr_in gossip_src(struct gossip* gossip) {
    return gossip->src;
}

char* gossip_latest(struct gossip* gossip) {
    return gossip->latest;
}

void print_my_gossips() {
    struct gossip *g;
    printf("\n---------------------\nPrinting my known gossips: \n");
    for(g = gossip; g != 0; g = g->next) {
        printf("%s\n", g->latest);
    }
    printf("---------------------\n\n");
}


/* A gossip message has the following format:
 *
 *  G<src_addr:src_port>/counter/payload\n
 *
 * Here <src_addr:src_port>/counter uniquely identify a message from
 * the given source.
 */
void gossip_received(struct file_info *fi, char *line){

    char *port = index(line, ':');
    if (port == 0) {
        fprintf(stderr, "do_gossip: format is G<addr>:<port>/counter/payload\n");
        return;
    }
    *port++ = 0;

    char *ctr = index(port, '/');
    if (ctr == 0) {
        fprintf(stderr, "do_gossip: no counter\n");
        return;
    }
    *ctr++ = 0;

    char *payload = index(ctr, '/');
    if (payload == 0) {
        fprintf(stderr, "do_gossip: no payload\n");
        return;
    }
    *payload++ = 0;

    /* Get the source and message identifier.
     */
    struct sockaddr_in addr;
    if (addr_get(&addr, line, atoi(port)) < 0) {
        return;
    }
    long counter = atol(ctr);

    /* See if we already have this gossip.
     */
    struct gossip *g;
    for (g = gossip; g != 0; g = g->next) {
        if (addr_cmp(g->src, addr) != 0) {
            continue;
        }
        if (g->counter >= counter) {
            printf("already know about this gossip\n");
            return;
        }
        free(g->latest);
        break;
    }
    if (g == 0) {
        g = calloc(1, sizeof(*g));
        g->src = addr;
        g->next = gossip;
        gossip = g;
    }

    /* Restore the line.
     */
    *--port = ':';
    *--ctr = '/';
    *--payload = '/';

    /* Save the gossip.
     */
    int len = strlen(line);
    g->latest = malloc(len + 1);
    memcpy(g->latest, line, len + 1);
    g->counter = counter;

    /* Send the gossip to all connections except the one it came in on.
     */
    char *msg = malloc(len + 3);
    sprintf(msg, "G%s\n", g->latest);
    file_broadcast(msg, len + 2, fi);
    free(msg);
}

// To add an address.
void add_to_queue(struct sockaddr_in x) {
    struct node* temp = (struct node*)malloc(sizeof(struct node));
    temp->addr = x; 
    temp->next = NULL;
    if(first == NULL && last == NULL){
        first = last = temp;
        return;
    }
    last->next = temp;
    last = temp;
}

// To remove an address.
struct node* remove_from_queue() {
    struct node* tmp = first;
    if(first == NULL) return NULL;
    if(first == last) {
        first = last = NULL;
        return tmp;
    }
    else {
        first = first->next;
    }
    return tmp;
}



// Use breadth first search to rebuild the graph from scratch. 
void build_graph(struct file_info *file_info) {
    node_no = 1;
    struct gossip *g, *go;
    char *p_addr, *payload;
    const char s[2] = ";";
    struct file_info *fi;

    if(nl != NULL) { nl_destroy(nl); }
    nl = nl_create();
    nl_add(nl, addr_to_string(my_addr));

    for (g = gossip; g != 0; g = g->next) 
    {
        if(sockaddr_to_file(g->src) != NULL) 
        {
            struct sockaddr_in root = g->src;
            add_to_queue(root);
            struct node* current;

            while(first != NULL) 
            {
                current = remove_from_queue();
                char* curr = addr_to_string(current->addr);
                if(nl_index(nl, curr) == -1) 
                {
                    nl_add(nl, curr);
                    node_no++;
                    for (go = gossip; go != 0; go = go->next) 
                    {
                        if(addr_cmp(current->addr, go->src) == 0) 
                        {
                            char *payload_start = index(go->latest, ';');
                            if(payload_start == 0) continue;
                            char *payload_copy = calloc(strlen(payload_start) + 1, sizeof(char));
                            strcpy(payload_copy, payload_start);
                            p_addr = strtok(payload_copy, s);
                            while(p_addr != NULL) 
                            {
                                add_to_queue(string_to_addr(p_addr));
                                p_addr = strtok(NULL, s);
                            }
                            free(payload_copy);
                        }
                    }
                }
            }
        }
    }

    dist = malloc(node_no * sizeof(int));
    prev = malloc(node_no * sizeof(int));
    graph = malloc(node_no * node_no * sizeof(int));

    for (g = gossip; g != 0; g = g->next) {
        if(addr_cmp(gossip->src, my_addr) != 0) 
        {
            char *payload_start = index(g->latest, ';');
            if(payload_start == 0) continue;
            char *payload_copy = calloc(strlen(payload_start) + 1, sizeof(char));
            strcpy(payload_copy, payload_start);
            p_addr = strtok(payload_copy, s);
            while(p_addr != NULL) 
            {
                char* tmp = addr_to_string(g->src);
                set_dist(nl, graph, node_no, tmp, p_addr, 1);
                p_addr = strtok(NULL, s);
                free(tmp);
            }
        }
    }
}


/* Send all gossip I have to the given peer.
 */
void gossip_to_peer(struct file_info *fi){
    struct gossip *g;

    for (g = gossip; g != 0; g = g->next) {
        file_info_send(fi, "G", 1);
        file_info_send(fi, g->latest, strlen(g->latest));
        file_info_send(fi, "\n", 1);
    }
}
