#include <arpa/inet.h>

double timer_now(void);
void timer_start(double when, void (*handler)(void *arg), void *arg);
int timer_check(void);

#define UNDEFINED               (-1)
#define INDEX(x, y, nnodes)     ((x) + (nnodes) * (y))

struct file_info;
struct sockaddr_in;
struct gossip;
struct node_list;
struct node {
	struct sockaddr_in addr;
	struct node *next;
};

struct node_list* nl;
int *dist;
int *prev;
int *graph;

typedef enum file_info_type {
    FI_FREE,                            
    FI_FILE,                           
    FI_SERVER,                          
    FI_OUTGOING,                        
    FI_INCOMING,                        
} type; 

void route_message(struct file_info* fi, char *line);


struct file_info* get_next_file(struct file_info* fi);
int get_file_type(struct file_info* fi);
struct sockaddr_in get_peer_addr(struct file_info* fi);
enum file_info_type get_file_type_enum(struct file_info *fi);
int get_union_status(struct file_info *fi);
char* get_file_uid(struct file_info *fi);


void gossip_to_peer(struct file_info *fi);
void gossip_received(struct file_info *fi, char *line);
struct gossip* gossip_next(struct gossip* gossip);
struct sockaddr_in gossip_src(struct gossip* gossip);
char* gossip_latest(struct gossip* gossip);
void build_graph();

char* addr_to_string (struct sockaddr_in addr);
struct sockaddr_in string_to_addr(char* string);
void set_dist(struct node_list *nl, int graph[], int nnodes, char *src, char *dst, int dist);

void file_info_send(struct file_info *fi, char *buf, int size);
void file_broadcast(char *buf, int size, struct file_info *fi);
struct file_info* sockaddr_to_file(struct sockaddr_in dst);

int addr_get(struct sockaddr_in *sin, const char *addr, int port);
int addr_cmp(struct sockaddr_in a1, struct sockaddr_in a2);


int nl_index(struct node_list *nl, char *node);
char *nl_name(struct node_list *nl, int index);
void nl_add(struct node_list *nl, char *node);
void nl_destroy(struct node_list *nl);
struct node_list *nl_create(void);
int nl_nsites(struct node_list *nl);
void dijkstra(int graph[], int nnodes, int src, int dist[], int prev[]);


