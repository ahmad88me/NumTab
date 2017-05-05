# Bash commands to adjust the Wikidata dump. 
# We are using wikidata-20170503-truthy-BETA.nt.bz2 
# Since the properties we are looking for should have only numerical values as domain, we limit the dump to those
bzcat dump.nt.bz2 | head -100 | awk '$3~/[0-9]/{print $3}'
bzcat dump.nt.bz2 | head -10000 | awk '$3~/\^\^\<http:\/\/www.w3.org\/2001/{print $0}'
bzcat dump.nt.bz2 | head -10000 | awk '$3~/\^\^\<http:\/\/www.w3.org\/2001/{print $0}' | sed -E 's/[<>"]//g' | sed -E 's/\^\^http:\/\/www.w3.org\/2001\/XMLSchema\#[a-zA-Z]+//g'
bzcat dump.nt.bz2 | head -10000 | awk '$2~/http:\/\/www.wikidata.org\/prop\/direct/{print $0}' | awk '$3~/\^\^\<http:\/\/www.w3.org\/2001/{print $0}' | sed -E 's/[<>"]//g' | sed -E 's/\^\^http:\/\/www.w3.org\/2001\/XMLSchema\#[a-zA-Z]+//g' | sed -E 's/\+//g' | sed -E 's/Z ././g'



bzcat dump.nt.bz2 | head -10000 | awk '$2~/http:\/\/www.wikidata.org\/prop\/direct/{print $0}' | sed '/entity\/Q[0-9]+> ./d' | sed -E 's/[<>"]//g' | sed -E 's/\^\^http:\/\/www.w3.org\/2001\/XMLSchema\#[a-zA-Z]+//g' | sed -E 's/\+//g' | sed -E 's/Z ././g'

# We know the set of properties, so we limit the dump to statements that use that statement  