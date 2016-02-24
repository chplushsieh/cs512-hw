# datapath = 'toy_example/'
datapath = 'dblp_4area/'

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
