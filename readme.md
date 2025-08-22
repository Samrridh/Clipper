**Memory optimized Clipboard Manager with EXTRA FEATURES!**

feature:
1. clipboard functionality

1. search option - find old text easily 
2. delete option - removes the item from history
3. pin option - option for pinning important text
4. show history - It doesn't store items in-memory, rather in json file to reduce ram as well as retain history
5. Sensitive Button - click item and then sensitive button, it will delete the item in 30sec for extra security

Optimisation:
1. Store items in json file rather than in ram
2. Deduplication implemented to avoid multiple same items
3. History capped at 50 items to save ram
4. Polls clipboard every 1 second rather than background threading