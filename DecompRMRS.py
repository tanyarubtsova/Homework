### Sagemath library is used here! 
#
# parameters:
# 2r < m - 1 (r > 1)
# k_RM = l * k_RS
#
#RM - parameters
r, m = 4, 9 #these parameters are changable
n_RM, k_RM = 2^m, 0
for i in range(0, r + 1):
    k_RM += binomial(m,i)
k_RM = k_RM - 0 # for cutting the Reed-Muller code
#   
#RS - parameters
l = 7 # and this parameter is changable
q = 2^l
n_RS, k_RS = q - 1, k_RM / l
#
print("RM:", n_RM, k_RM)
print("RS:", n_RS, k_RS)
print("RS2:", n_RS * l, k_RS * l)
#
#RM - code   
C_RM = codes.BinaryReedMullerCode(r, m)
E_RM = codes.encoders.ReedMullerVectorEncoder(C_RM)
G_RM = E_RM.generator_matrix()
print(C_RM)
print(type(G_RM), G_RM)
print()
#
#RS - code
C_RS = codes.ReedSolomonCode(GF(q), n_RS, k_RS); 
E_RS = codes.encoders.GRSEvaluationVectorEncoder(C_RS);
G_RS = E_RS.generator_matrix();
print(C_RS)
print(G_RS)
print()
#
#RS_2 - code
n_RS2 = n_RS * l
k_RS2 = k_RS * l
M = MatrixSpace(GF(2), k_RS2, n_RS2)
G_RS2 = M.matrix()
field = (G_RS[0][0]).parent()
gen = field._cache.gen()
for i in range(k_RS):
    vec = []
    for k in range(l):
        vec.append([])
    for j in range(n_RS):
        el = G_RS[i][j]
        for k in range(l):
            el_pol = el.polynomial()
            el_vec = el_pol.list()
            el_vec += [0] * (l - 1 - el_pol.degree())
            vec[k]  += el_vec
            el = field._cache.a_times_b_minus_c(el, gen, field(0))
    for k in range(l):
        G_RS2[i * l + k] = vector(vec[k])
print("G_RS2:", type(G_RS2))
print(G_RS2)
print()
#
M2 = MatrixSpace(GF(2), k_RM, n_RM)
G_RM2 = M2.matrix()
for i in range(k_RM):
    G_RM2[i]=G_RM[i] # for cutting the Reed-Muller code
#
#RMRS - code
n_RMRS = n_RM + n_RS2
k_RMRS = k_RS2 
G = G_RM2.augment(G_RS2, subdivide=True)
print("G:", type(G))
print(G)
#
#GG=G_RMRS^2 - Schur/Hadamar product RMRS)
kk = binomial(k_RMRS + 1, 2)
MM = MatrixSpace(GF(2), kk, n_RMRS)
print("MM:", MM)
GG = MM.matrix()
ii = 0
for i in range(k_RMRS):
    for j in range(i, k_RMRS):
        vec = [0] * n_RMRS
        for k in range(n_RMRS):
            vec[k] = G[i][k] and G[j][k]
        vec = vector(vec)
        GG[ii] = vec
        ii += 1
print("GG1:", GG.rank(), type(GG))
print(GG)
#
#GG_RM=G_RM^2 - Schur/Hadamar product RM)
kk_RM = binomial(k_RM + 1, 2)
MM_RM = MatrixSpace(GF(2), kk_RM, n_RM)
print("MM_RM:", MM_RM)
GG_RM = MM_RM.matrix()
ii = 0
for i in range(k_RM):
    for j in range(i, k_RM):
        vec = [0] * n_RM
        for k in range(n_RM):
            vec[k] = G_RM[i][k] and G_RM[j][k]
        vec = vector(vec)
        GG_RM[ii] = vec
        ii += 1
print("GG_RM:", GG_RM.rank())
#
#GG_RS=G_RS^2 - Schur/Hadamar product RS2)
kk_RS = binomial(k_RS2 + 1, 2)
MM_RS = MatrixSpace(GF(2), kk_RS, n_RS2)
print("MM_RS:", MM_RS)
GG_RS = MM_RS.matrix()
ii = 0
for i in range(k_RS2):
    for j in range(i, k_RS2):
        vec = [0] * n_RS2
        for k in range(n_RS2):
            vec[k] = G_RS2[i][k] and G_RS2[j][k]
        vec = vector(vec)
        GG_RS[ii] = vec
        ii += 1
print("GG_RS:", GG_RS.rank())
#
#Decomposition algorythm
GG = GG.rref()
rank = GG.rank()
print("GG:", GG.rank())
print(GG)
#
VV = {i for i in range(rank)}
V = []
W = []
B = []
for j in range(rank):
    if VV.issuperset({j}):
        V_i = {j}
        W_i = GG[j]
        changed = True    
        while changed:
            changed = False
            tmpVV = VV - {j}
            for l in tmpVV:
                vec0 = [0] * n_RMRS
                vec = [0] * n_RMRS
                for k in range(n_RMRS):
                    vec[k] = W_i[k] and GG[l][k]
                changed2 = False
                if vec != vec0:
                    for k in range(n_RMRS):
                        if GG[l][k] > W_i[k]: 
                            changed2 = True
                if changed2:
                    changed = True
                    V_i.add(l)
                    for k in range(n_RMRS):
                        vec[k] = W_i[k] or GG[l][k]
                    W_i = vec             
        B_i = {GG[i] for i in V_i}
        VV -= V_i
        V.append(V_i)
        W.append(W_i)
        B.append(B_i)
print("V:", len(V))
print(V)
print("W:", W)
print("B:", B)
