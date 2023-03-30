'''The algorithm for solving this task will aim to minimize the number of starting points so that later invocations of BFS can handle the vast state space.
Depending on the complexity of the wall arrangement on the board, BFS can find a solution for 2-3 starting points in a reasonable time, so it will
be necessary to ensure that it gets a maximum of 2-3 vertices. The strategy for eliminating starting points is as follows:

Phase I: It moves in a circle (let the board have dimensions n x m) by making n moves up and down and m moves left and right, in the order ULDR.
Phase II: If there are still too many points on the board, and if any two points are in the same column or row or have a small distance between them, then it will merge them.
Phase III: It invokes BFS on the remaining starting points on the board'''

import time

start = time.time()

# to the result needed, determines the moves
def letter(l):
    U = [-1, 0]
    L = [0, -1]
    R = [0, 1]
    D = [1, 0]
    if l == U:
        return "U"
    elif l == L:
        return "L"
    elif l == R:
        return "R"
    elif l == D:
        return "D"

# B - state of the board as set, move - UDLR, amount - number of moves towards move, s is a set composed of wall points
def update(B, ruch, ilosc, s):
    h = [1, 1]
    res = set()
    addset = set()
    ruchy = ''
    for i in range(0, ilosc):
        ruchy += letter(ruch)
        res = set()
        addset = set()
        for j in B:
            h[0], h[1] = j
            if (ruch[0]+h[0], ruch[1]+h[1]) not in s and ruch[0]+h[0] >= 0 and ruch[0]+h[0] < n and ruch[1]+h[1] >= 0 and ruch[1]+h[1] < m:
                res.add((ruch[0]+h[0], ruch[1]+h[1]))
            else:
                addset.add(j)

        B = res.union(addset)
    return B, ruchy


def first_phase(B, n, m, s):
    U = [-1, 0]
    L = [0, -1]
    R = [0, 1]
    D = [1, 0]
    B, res1 = update(B, U, n, s)
    B, res2 = update(B, L, m, s)
    B, res3 = update(B, D, n, s)
    B, res4 = update(B, R, m, s)
    return B, res1+res2+res3+res4


def find(Bb, s):
    result = ''
    Dd = Bb.copy()
    queue = []
    S = Bb.copy()
    B = S.copy()
    while Dd:
        if len(Dd) == 1:
            break
        i = Dd.pop()
        k = len(S)
        find = 1
        while k > 0:
            if find == 1:
                B = S.copy()
                find = 0
            if len(B) == 0:
                break
            else:
                h = B.pop()
            if h != i and (h[0] == i[0] or h[1] == i[1] or abs(h[0] - i[0])+abs(h[1] - i[1]) < 9):
                queue = []
                visited = {}
                v = []
                v.append(i)
                v.append(h)
                idp = 0
                idk = 0
                queue.append(("", v, S))
                visited[tuple(v)] = 1
                while idp != idk+1:
                    w = queue[idp]
                    if len(w[1]) == 1:
                        result += w[0]
                        find = 1
                        k = len(w[2])+1
                        Dd = w[2]
                        S = w[2].copy()
                        for j in w[1]:
                            i = j
                        idp = idk
                    else:
                        U = [-1, 0]
                        L = [0, -1]
                        R = [0, 1]
                        D = [1, 0]
                        a1 = update(w[1], U, 1, s)[0]
                        a2 = update(w[1], L, 1, s)[0]
                        a3 = update(w[1], D, 1, s)[0]
                        a4 = update(w[1], R, 1, s)[0]
                        B1, res1 = update(w[2], U, 1, s)
                        B2, res2 = update(w[2], L, 1, s)
                        B3, res3 = update(w[2], D, 1, s)
                        B4, res4 = update(w[2], R, 1, s)
                        if visited.get(tuple(a1)) == None or visited.get(tuple(a1)) != 1:
                            queue.append((w[0]+"U", a1, B1))
                            visited[tuple(a1)] = 1
                            idk += 1
                        if visited.get(tuple(a2)) == None or visited.get(tuple(a2)) != 1:
                            queue.append((w[0]+"L", a2, B2))
                            visited[tuple(a2)] = 1
                            idk += 1
                        if visited.get(tuple(a3)) == None or visited.get(tuple(a3)) != 1:
                            queue.append((w[0]+"D", a3, B3))
                            visited[tuple(a3)] = 1
                            idk += 1
                        if visited.get(tuple(a4)) == None or visited.get(tuple(a4)) != 1:
                            queue.append((w[0]+"R", a4, B4))
                            visited[tuple(a4)] = 1
                            idk += 1
                    idp += 1
            k = k-1
    return S, result


# output of a state
def print_all(B, g, s, n, m):
    for i in range(0, n):
        for j in range(0, m):
            if (i, j) in s:
                print("#", end='')
            elif (i, j) in B:
                print("B", end='')
            elif (i, j) in g:
                print("G", end='')
            else:
                print(" ", end='')
        print()


# reading input data
plik = open('zad_input.txt', "r")
tab = []
for linia in plik:
    list = linia.split()
    tab.append(list[0])

B = set()
g = set()
s = set()
n = len(tab)
m = len(tab[0])
for i in range(0, n):
    for j in range(0, m):
        if tab[i][j] == '#':
            s.add((i, j))
        elif tab[i][j] == 'G':
            g.add((i, j))
        elif tab[i][j] == 'B':
            B.add((i, j))
            g.add((i, j))
        elif tab[i][j] == 'S':
            B.add((i, j))


B, res1 = first_phase(B, n, m, s)
B, res2 = find(B, s)


def finish(w, D):
    for e in w:
        if e not in D:
            return False
    return True


def bfs(B, g):
    queue = []
    v = []
    for i in B:
        v.append(i)
    idp = 0
    idk = 0
    queue.append(("", v))
    visited = {}
    visited[tuple(v)] = 1
    while idp != idk+1:
        w = queue[idp]
        if finish(w[1], g):
            return w[0], w[1]
        else:
            U = [-1, 0]
            L = [0, -1]
            R = [0, 1]
            D = [1, 0]
            a1 = update(w[1], U, 1, s)[0]
            a2 = update(w[1], L, 1, s)[0]
            a3 = update(w[1], D, 1, s)[0]
            a4 = update(w[1], R, 1, s)[0]
            if visited.get(tuple(a1)) == None or visited.get(tuple(a1)) != 1:
                queue.append((w[0]+"U", a1))
                visited[tuple(a1)] = 1
                idk += 1
            if visited.get(tuple(a2)) == None or visited.get(tuple(a2)) != 1:
                queue.append((w[0]+"L", a2))
                visited[tuple(a2)] = 1
                idk += 1
            if visited.get(tuple(a3)) == None or visited.get(tuple(a3)) != 1:
                queue.append((w[0]+"D", a3))
                visited[tuple(a3)] = 1
                idk += 1
            if visited.get(tuple(a4)) == None or visited.get(tuple(a4)) != 1:
                queue.append((w[0]+"R", a4))
                visited[tuple(a4)] = 1
                idk += 1
        idp += 1


res = ''
bfss, dest_state = bfs(B, g)
res += bfss
end = time.time()
print(end - start)

# saving the results to an output file
filee = open("zad_output.txt", "w")
filee.write(res1+res2+res)
filee.close()
