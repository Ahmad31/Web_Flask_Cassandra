# Web_Flask_Cassandra

# Configurasi Docker
Menggunakan private cloud dengan Docker, untuk memanipulasi topologi 
Ada 3 Container yang dibuat dari images Ubuntu.15.04

## Ambil Images Ubuntu.15.04

            sudo docker pull ubuntu:15.04

## Buat Container dengan nama cassandra-server1 sebagai node1
            sudo docker run -d -i -p 5052:22 --ulimit nofile=100000:100000 --ulimit memlock=-1:-1 --ulimit nproc=32768:32768 --name="cassandra-server1" ubuntu:15.04 /bin/bash
            
## Buat Container dengan nama cassandra-server2 sebagai node2
            sudo docker run -d -i -p 5053:23 --ulimit nofile=100000:100000 --ulimit memlock=-1:-1 --ulimit nproc=32768:32768 --name="cassandra-server2" ubuntu:15.04 /bin/bash
            
## Buat Container dengan nama cassandra-server3 sebagai node3
            sudo docker run -d -i -p 5054:24 --ulimit nofile=100000:100000 --ulimit memlock=-1:-1 --ulimit nproc=32768:32768 --name="cassandra-server3" ubuntu:15.04 /bin/bash

# Install Cassandra versi 3.11
## Instal pada masing-masing container Docker:
            
            root# echo "deb http://www.apache.org/dist/cassandra/debian 311x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
            
            root# curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -

            $ apt-get update
            
            $ sudo apt-get install cassandra
            
## Configurasi file /etc/cassandra/cassandra.yaml disetiap container Docker:

            ........
            cluster_name: 'Arsip Dokument'
            ........
            # seeds is actually a comma-delimited list of addresses.
            # Ex: "<ip1>,<ip2>,<ip3>"
            - seeds: "172.17.0.2,172.17.0.3,172.17.0.4"     #ini diisi dengan alamat IP masing-masing node1, node2, node3
            ........
            listen_address: 172.17.0.2                      #Awalnya "localhost", diganti IP masing-masing node, node1(172.17.0.2), node2(172.17.0.3), node3(172.17.0.4)
            ........
            rpc_address: localhost                          #Awalnya "localhost", diganti IP masing-masing node, node1(172.17.0.2), node2(172.17.0.3), node3(172.17.0.4)

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

## Catatan 



             
             
               

            
