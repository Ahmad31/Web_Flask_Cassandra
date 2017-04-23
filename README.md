# Web_Flask_Cassandra

# Install Cassandra repo Datastax-ddc

Datastax-ddc free dikeluarkan oleh Datastax https://academy.datastax.com/planet-cassandra/cassandra, Cassandra Datastax Community sudah tidak didukung, datastax-ddc sebagai pengganti versi gratis.

Menggunakan private cloud dengan Docker, untuk memanipulasi topologi

Ada 3 Container yang dibuat dari images Ubuntu.15.04


## Instal pada masing-masing container Docker:
            
            root# echo "deb http://debian.datastax.com/datastax-ddc 3.4 main" | tee -a /etc/apt/sources.list.d/cassandra.sources.list
            
            root# curl -L https://debian.datastax.com/debian/repo_key | apt-key add -

            $ apt-get update
            
            $ apt-get install datastax-ddc
            
## Configurasi file /etc/cassandra/cassandra.yaml disetiap container Docker:

            ........
            cluster_name: 'Arsip Dokument'
            ........
            # seeds is actually a comma-delimited list of addresses.
            # Ex: "<ip1>,<ip2>,<ip3>"
            - seeds: "172.17.0.2,172.17.0.3,172.17.0.4"     #ini diisi dengan alamat IP masing-masing node1, node2, node3
            ........
            listen_address: 172.17.0.2                      #Awalnya "localhost", diganti IP masing-masing node, ini node1
            ........
            rpc_address: localhost                          #Awalnya "localhost", diganti IP masing-masing node, ini node1

## Menjalankan Cassandra :
          
             root# service cassandra start
             
             
             root# service cassandra status
               * Cassandra is running
               
             root# nodetool status
             Datacenter: datacenter1
             =======================
             Status=Up/Down
             |/ State=Normal/Leaving/Joining/Moving
              --  Address     Load       Tokens       Owns (effective)  Host ID                               Rack
             UN  172.17.0.2  127.61 KB  256          100.0%            de0e020c-8e1a-4b97-b7d8-18bb4239b4a9  rack1

## Catatan *
Dalam mode pengembangan web, yang saya pakai hanya node1 terlebih dahulu, agar lebih memudahkan dan tidak membuat berat
karna menjalankan 3 container sekaligus perlu RAM diatas 4GB


             
             
               

            
