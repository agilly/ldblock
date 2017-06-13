#!/nfs/team144/jupyter/bin/python

import pandas as pd
import sys
import numpy as np

d=pd.read_table(sys.argv[1])
d.columns=['id', 'ps', 'p']
d.sort_values("p", inplace=True)

ld=pd.read_table(sys.argv[2], sep='\s+')
d['block']=0

s=d.id[0]

nextblock=1
for index, row in d.iterrows():
	if d.ix[index, 'block'] > 0:
		continue
	d.loc[d['id'] == row['id'], 'block']=nextblock
	inld=ld.loc[ ((ld['SNP_A'] == row['id']) | (ld['SNP_B'] == row['id'])) & (ld['R2']>float(sys.argv[4])) ,]
	ids=np.r_[inld['SNP_A'], inld['SNP_B']]
	d.loc[d.id.isin(np.unique(ids)) & (d.block ==0), 'block']=nextblock
	nextblock=nextblock+1
d.loc[d.block>8, 'block']=0
d.to_csv(sys.argv[3], index=False)