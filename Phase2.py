import os
print("Phase 2")

btree_cmd = 'db_load -c duplicates=1 -T -t btree'
hash_cmd = 'db_load -T -t hash'

os.system( 'sort -u recs.txt  | perl break.pl | {} re.idx'.format(hash_cmd))
os.system( 'sort -u terms.txt | perl break.pl | {} te.idx'.format(btree_cmd))
os.system( 'sort -u emails.txt| perl break.pl | {} em.idx'.format(btree_cmd))
os.system( 'sort -u dates.txt | perl break.pl | {} da.idx'.format(btree_cmd))

print('Phase 2 Finished')