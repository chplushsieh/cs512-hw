# datapath = 'toy_example/'
datapath = 'dblp_4area/'

''' For p_pagerank.py '''

TELEPORT = 0.15
ITERATION_TIME = 10

''' For pathsim.py '''

'''
I changed line 32183 from:
32183	"Boosting'' a Positive-Data-Only Learner.
to:
32183	"Boosting" a Positive-Data-Only Learner.
because python csv reader can't parse a single unpaird double quote properly.
'''

TERM = 'term'
tmin = 1
tmax = 13575

PAPER = 'paper'
pmin = 13576
pmax = 42144

VENUE = 'venue'
vmin = 42145
vmax = 42164

AUTHOR = 'author'
amin = 42166
amax = 70865

'''

 matrixPT, matrixPV, matrixPA done

Time spent: 122.68872809410095

matrixAPV is loaded
Time spent: 0.03108501434326172

matrixAPVPA is loaded
Time spent: 5.881944179534912

The top similar authors to Christos Faloutsos using APVPA are:

68855    1.000000
46477    0.905782
42978    0.900862
55154    0.839144
67211    0.831342
48756    0.808531
46473    0.804048
68494    0.788012
50510    0.778708
43784    0.775447
69189    0.774464
Name: 68855, dtype: float64

The top similar authors to AnHai Doan using APVPA are:

51360    1.000000
44508    0.968215
47048    0.966921
49305    0.964187
50377    0.948207
63192    0.946524
57906    0.944123
57948    0.943867
47041    0.936639
53849    0.936416
44505    0.934132
Name: 51360, dtype: float64

matrixAPT is loaded
Time spent: 4.0002429485321045

matrixAPTPA is saved
Time spent: 1.0299019813537598

The top similar authors to Xifeng Yan using APTPA are:

66631    1.000000
42240    0.747253
57482    0.636583
56166    0.617843
53833    0.608368
68305    0.603600
42677    0.600402
70441    0.570320
67211    0.558499
67500    0.547226
44101    0.525301
Name: 66631, dtype: float64

The top similar authors to Jamie Callan using APTPA are:

59090    1.000000
69963    0.626344
64200    0.586319
68273    0.585987
63972    0.572178
70713    0.566632
68491    0.565289
44132    0.562914
51452    0.561039
56924    0.554839
46626    0.551509
Name: 59090, dtype: float64

'''
