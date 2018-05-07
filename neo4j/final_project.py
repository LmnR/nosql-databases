# Put the use case you chose here. Then justify your database choice:
# Instagram was the use case I chose - since many of the objects in this use case are relationships with few/no properties e.g. likes, 
# I felt that the graph model for neo4j was effective for storing and querying relationships - even though neo4J is not optimized for large scale querying 
# or queries spanning a large part of the database (which might be a problem due to the scale of an app like Instagram), I feel like the consantly involving 
# nature of Instagram with new products needing to be added (think Stories) demands a flexible database like neo4j
#
# Explain what will happen if coffee is spilled on one of the servers in your cluster, causing it to go down.
# Since all the instances in the cluster have full copies of the data, if an instance goes down due to the coffee, it will be marked as temporarily failed, 
# and operations will continue. If the instance was a master, a new one will be elected. When the downed instance becomes available again, it will automatically
# catch up with the cluster.
#
# What data is it not ok to lose in your app? What can you do in your commands to mitigate the risk of lost data?
# User data would be the most important data to not lose in the app (users might have local copies of photos, etc.), and so data such as username, password, etc. cannot be lost.
# Good practices may be to constantly back up user data.

from neo4j.v1 import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "test"))

def project():
    user_count = 3
    current_time = '600'
    time = int(current_time)

    with driver.session() as session:
        with session.begin_transaction() as tx:
            tx.run("MATCH (n)"
                   "DETACH DELETE n")
            print("db cleared")

            tx.run("CREATE (n1:User {id: 1, name: 'Jin Peng', username: 'jinjpeng', password: 'iloveanna'});")
            tx.run("CREATE (n2:User {id: 2, name: 'Anna Chen', username: 'annachen', password: 'iloveannatoo'});")
            tx.run("CREATE (n3:User {id: 3, name: 'Jerry Cat', username: 'jerrycat', password: 'jinsucks'});")

            tx.run("CREATE (n4:Photo {id: 4, caption: 'beautiful sunset! #beach'});")
            # tx.run("CREATE (n5:Photo {id: 5, caption: 'look at this ice cream'});")
            # tx.run("CREATE (n6:Photo {id: 6, caption: 'i miss my owner'});")

            tx.run("CREATE (n7:Comment {id: 7, comment: 'when r u comin back'});")
            tx.run("CREATE (n8:Comment {id: 8, comment: 'wish i was here!!!'});")
            # tx.run("CREATE (n9:Comment {id: 9, comment: 'how is jin'});")

            tx.run("MATCH (a:Photo),(b:User) "
                   "WHERE a.id = 4 AND b.id = 1 "
                   "CREATE (a)-[r:POSTED_BY {date_posted: '500'}]->(b);")

            tx.run("MATCH (a:Photo),(b:Comment) "
                   "WHERE a.id = 4 AND b.id = 7 "
                   "CREATE (a)-[r:HAS_COMMENT {date_posted: '505'}]->(b);")

            tx.run("MATCH (a:Photo),(b:Comment) "
                   "WHERE a.id = 4 AND b.id = 8 "
                   "CREATE (a)-[r:HAS_COMMENT {date_posted: '501'}]->(b);")

            tx.run("MATCH (a:Photo),(b:User) "
                   "WHERE a.id = 4 AND b.id = 2 "
                   "CREATE (a)-[r:LIKED_BY {date_liked: '501'}]->(b);")

            tx.run("MATCH (a:Comment),(b:User) "
                   "WHERE a.id = 7 AND b.id = 3 "
                   "CREATE (a)-[r:COMMENTED_BY {date_posted: '505'}]->(b);")

            tx.run("MATCH (a:Comment),(b:User) "
                   "WHERE a.id = 8 AND b.id = 2 "
                   "CREATE (a)-[r:COMMENTED_BY {date_posted: '501'}]->(b);")

            tx.run("MATCH (a:User),(b:User) "
                   "WHERE a.id = 1 AND b.id = 2 "
                   "CREATE (a)-[r:FOLLOWED_BY {since: '300'}]->(b);")

            tx.run("MATCH (a:User),(b:User) "
                   "WHERE a.id = 1 AND b.id = 3 "
                   "CREATE (a)-[r:FOLLOWED_BY {since: '100'}]->(b);")

            tx.run("MATCH (a:User),(b:User) "
                   "WHERE a.id = 2 AND b.id = 1 "
                   "CREATE (a)-[r:FOLLOWED_BY {since: '300'}]->(b);")

            tx.run("MATCH (a:User),(b:User) "
                   "WHERE a.id = 2 AND b.id = 3 "
                   "CREATE (a)-[r:FOLLOWED_BY {since: '400'}]->(b);")

            tx.run("MATCH (a:User),(b:User) "
                   "WHERE a.id = 3 AND b.id = 1 "
                   "CREATE (a)-[r:FOLLOWED_BY {since: '100'}]->(b);")

            tx.run("MATCH (a:User),(b:User) "
                   "WHERE a.id = 3 AND b.id = 2 "
                   "CREATE (a)-[r:FOLLOWED_BY {since: '400'}]->(b);")

            # Action 1: User signs up for account
            user_count += 1
            tx.run("CREATE (n1:User {id: {count}, name: 'Tom Cat', username: 'tomcat', password: 'abc'});", count=user_count)

            # Action 2: User sees who his/her followers are
            for record in tx.run("MATCH (a:User)-[:FOLLOWED_BY]->(b:User) "
                                 "WHERE a.id = 1 "
                                 "RETURN b.name"):
                print(record["b.name"])

            # Action 3: User sees his/her photo captions
            for record in tx.run("MATCH (a:Photo)-[:POSTED_BY]->(b:User) "
                                 "WHERE b.id = 1 "
                                 "RETURN a.caption"):
                print(record["a.caption"])

            # Action 4: User likes a photo
            tx.run("MATCH (a:Photo),(b:User) "
                   "WHERE a.id = 4 AND b.id = 3 "
                   "CREATE (a)-[r:LIKED_BY {date_liked: {time}}]->(b);", time=time)

            # Action 5: User comments on a photo
            tx.run("CREATE (n9:Comment {id: 9, comment: 'hey what about me'});")
            tx.run("MATCH (a:Photo),(b:Comment) "
                   "WHERE a.id = 4 AND b.id = 9 "
                   "CREATE (a)-[r:HAS_COMMENT {date_posted: {time}}]->(b);", time=time)

            tx.run("MATCH (a:Comment),(b:User) "
                   "WHERE a.id = 9 AND b.id = 4 "
                   "CREATE (a)-[r:COMMENTED_BY {date_posted: {time}}]->(b);", time=time)

            # Action 6: User follows another user
            tx.run("MATCH (a:User),(b:User) "
                   "WHERE a.id = 1 AND b.id = 4 "
                   "CREATE (a)-[r:FOLLOWED_BY {since: {time}}]->(b);", time=time)            

            # Action 7: Users posts a photo
            tx.run("CREATE (n5:Photo {id: 5, caption: 'look at this ice cream'});")
            tx.run("MATCH (a:Photo),(b:User) "
                   "WHERE a.id = 5 AND b.id = 2 "
                   "CREATE (a)-[r:POSTED_BY {date_posted: {time}}]->(b);", time=time)

            # Action 8: User sees his/her comments
            for record in tx.run("MATCH (a:Comment)-[:COMMENTED_BY]->(b:User) "
                                 "WHERE b.id = 2 "
                                 "RETURN a.comment"):
                print(record["a.comment"])

project()
