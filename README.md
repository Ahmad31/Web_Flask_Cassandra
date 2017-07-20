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

## Insatal Java 8 dan vim, libevent-dev pada container "node1, node2, node3"
    sudo docker exec -ti cassandra-server apt-get update
    sudo docker exec -ti cassandra-server apt-get install iputils-ping telnet bridge-utils wget curl vim
    sudo docker exec -ti cassandra-server apt-get install libevent-dev aptitude net-tools

# Install Cassandra versi 3.8
## Instal pada masing-masing container Docker:
            
     root# echo "deb http://www.apache.org/dist/cassandra/debian 38x main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
            
     root# curl https://www.apache.org/dist/cassandra/KEYS | sudo apt-key add -

     root# apt-get update
            
     root# apt-get install cassandra
            
## Configurasi file /etc/cassandra/cassandra.yaml disetiap container:

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


## Membuat Keyspace dengan nama "arsip"
    # cqlsh.> CREATE KEYSPACE arsip
    WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
    
## Membuat Tabel dengan nama "dokumen"
-> Masuk Pada container "Cassandra-server1" dengan perintah
    
    # cqlsh 172.17.0.2
   
    CREATE TABLE dokumen (
    nim int,
    prodi text,
    tahun date,
    judul text,
    kata_kunci text,
    angkatan date,
    file1 text,
    file2 text,
    file3 text,
    file4 text,
    file5 text,
    intisari text,
    nama_mhs text,
    password text,
    pembimbing text,
    PRIMARY KEY (prodi,nim ));

## *Catatan
perintah pembuatan table hanya dilakukan satu kali saja pada server virtual, bisa dibuat disembarang server virtual node1, node2 atau node3.

## Sample Data
    # cqlsh 172.17.0.2
    
    # use arsip

    INSERT INTO doc1 (nim , prodi , tahun , judul , kata_kunci , angkatan , intisari , nama_mhs , pembimbing , password , file1, file2, file3, file4, file5 ) VALUES ( 135410091, 'Teknik Informatika', '2017-02-02', 'Arsip Dokumen dengan Cassandra implementasi Multi Node Single Cluster ', 'rsip Dokumen dengan Cassandra implementasi Multi Node Single Cluster', '2013-01-01', 'rsip Dokumen dengan Cassandra implementasi Multi Node Single Cluster', 'Ahmad Anwar', 'Bambang PDP', 'aku', 'data', 'data', 'data', 'data', 'data');

## Membuat Index SASI
Ini diguanakan untuk mengimplementasikan menu pencarian pada table dokumen berdasarkan jundul
       
    # CREATE CUSTOM INDEX cari_judul ON project.document ( judul ) USING 'org.apache.cassandra.index.sasi.SASIIndex' WITH OPTIONS = { 
    'analyzed' : 'true', 
    'analyzer_class' : 'org.apache.cassandra.index.sasi.analyzer.NonTokenizingAnalyzer', 
    'case_sensitive' : 'false', 
    'mode' : 'CONTAINS' 
    };


## Uji Coba mencari data dengan kata "cluster"
    cqlsh:project> SELECT * FROM document WHERE judul LIKE '%cluster%'


## Menjalan Program
- Instal semua keperluan untuk menjalankan framework Flask
- Instal Driver Cassandra
    
      root# pip3 install cassandra-driver
      root# apt-get install libev4 libev-dev
 
 - Instal CQLAlchemy
 
       root# pip install flask-cqlalchemy
 
- Masuk pada folder, ketik perintah
      
      arsip$ python run.py
- Membuka browser ketik url
      
      127.0.0.1:5000
      



             
             
               

            
