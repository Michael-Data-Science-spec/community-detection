from copy import deepcopy

class Louvain:
    def __init__(self, edge_dct):
        self.packed_communities = []
        self.edge_dct = self.add_weight(edge_dct)
        # print(self.edge_dct)
        self.make_undirected()
        self.process_graph()

    def get_m2(self):
        num = 0
        for u in self.edge_dct:
            for _, _ in self.edge_dct[u]:
                num += 1
        self.m2 = num

    def add_weight(self, edge_dct):
        unrepresented = set()

        for u in edge_dct:
            for idx, v in enumerate(edge_dct[u]):
                if type(v) != tuple:
                    edge_dct[u][idx] = (v, 1)

                v = edge_dct[u][idx][0]
                if v not in edge_dct:
                    unrepresented.add(v)

        while unrepresented:
            v = unrepresented.pop()
            edge_dct[v] = []
        return edge_dct

    def make_undirected(self):
        for u in self.edge_dct:
            for idx, e in enumerate(self.edge_dct[u]):
                v, d = e
                if (u, d) not in self.edge_dct[v]:
                    self.edge_dct[v].append((u, d))

    def create_communities(self):
        communities = {x: set([x]) for x in self.edge_dct}
        self.communities = communities

    def get_edge_degrees(self):
        edge_degrees = {x: sum(map(lambda x: x[1], self.edge_dct[x])) for x in self.edge_dct}
        self.edge_degrees = edge_degrees

    def assign_communities(self):
        node_community = {x: x for x in self.edge_dct}
        self.node_community = node_community

    def get_in_degrees(self):
        in_degrees = {x: 0 for x in self.communities}

        for u in self.edge_dct:
            c = self.node_community[u]

            for v, d in self.edge_dct[u]:
                if v in self.communities[u]:
                    in_degrees[c] += d

        self.in_degrees = in_degrees

    def process_graph(self, weighted=False):
        self.create_communities()
        self.get_edge_degrees()
        self.assign_communities()
        self.get_in_degrees()
        self.get_m2()

    def louvain(self):
        while True:
            idx = 0
            changes = True

            while changes == True:
                idx += 1
                changes = self.reassign_communities()

            empty_communities = []
            for c in self.communities:
                if self.communities[c] == set():
                    empty_communities.append(c)

            for c in empty_communities:
                del self.communities[c]

            for c in self.communities:
                self.communities[c] = list(self.communities[c])

            
            # self.communities = {i: value for i, value in enumerate(self.communities.values())}
            # print(self.communities)

            self.packed_communities.append(deepcopy(self.communities))

            new_G = self.deprecate_communities()
            self.edge_dct = new_G
            self.process_graph()

            if idx == 1:
                break

        return self.packed_communities

    def reassign_communities(self):
        changes = False

        for u in self.edge_dct:
            c = self.node_community[u]
            self.reassign_community(u, c)
            if self.node_community[u] != c:
                changes = True

        return changes

    def reassign_community(self, v, c):
        new_c = self.optimal_c(v)[1]
        self.node_community[v] = new_c
        self.communities[c].remove(v)
        self.communities[new_c].add(v)

    def optimal_c(self, v):
        best_q, best_c = 0, self.node_community[v]
        for u, _ in self.edge_dct[v]:
            new_c = self.node_community[u]

            if best_c == new_c:
                continue

            new_q = self.delta_Q(v, new_c, best_c)
            if new_q > best_q:
                best_q, best_c = new_q, new_c

        return best_q, best_c

    def deprecate_communities(self):
        new_G = {x: list() for x in self.communities if len(self.communities[x]) > 0}

        for c in self.communities:
            comm_edges = {c: 0}
            for u in self.communities[c]:
                for v, d in self.edge_dct[u]:
                    c_v = self.node_community[v]
                    if c_v == c:
                        comm_edges[c] += d
                    elif c_v in comm_edges:
                        comm_edges[c_v] += d
                    else:
                        comm_edges[c_v] = d

            if comm_edges[c] == 0 and len(comm_edges.keys()) == 1:
                continue

            new_G[c] = list(comm_edges.items())

        return new_G

    def delta_Q(self, v, c1, c2):
        Q = 2 * self.m2 * (self.calc_k(v, c1) - self.calc_k(v, c2))
        Q += 2 * self.edge_degrees[v] * (self.edges_total(c2) - self.edges_total(c1) - self.edge_degrees[v])
        Q /= self.m2 ** 2
        return Q

    def cycles(self, v):
        cycle = 0
        for u, _ in self.edge_dct[v]:
            if u == v:
                cycle += 1

        return cycle

    def calc_k(self, v, c):
        k = self.cycles(v)
        for u, d in self.edge_dct[v]:
            if self.node_community[u] == c:
                k += d

        return k

    def edges_total(self, c):
        total = 0
        for v in self.communities[c]:
            total += self.edge_degrees[v]

        return total


if __name__ == "__main__":
    edge_dct = {
        1: [2, 4],
        2: [1, 3, 4],
        3: [2, 4, 8],
        4: [1, 2, 3, 6],
        5: [6, 7, 8, 9],
        6: [4, 6, 7, 8, 9],
        7: [5, 6, 8, 9],
        8: [],
        9: [],
    }
    l = Louvain(edge_dct)
    print(l.louvain())