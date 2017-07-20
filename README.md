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
    sudo docker exec -ti cassandra-server1 apt-get update
    sudo docker exec -ti cassandra-server1 apt-get install iputils-ping telnet bridge-utils wget curl vim
    sudo docker exec -ti cassandra-server1 apt-get install libevent-dev aptitude net-tools

# Install Cassandra versi 3.8
## Instal pada masing-masing container Docker:
     
     docker exec -ti cassandra-server1 bash
            
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
            - seeds: "172.17.0.2,172.17.0.3,172.17.0.4"     #ini diisi dengan alamat IP semua node yang akan digabungkan kedalam cluster/datacenter node1, node2, node3
            ........
            listen_address: 172.17.0.2                      #Awalnya "localhost", diganti IP masing-masing node, node1(172.17.0.2), node2(172.17.0.3), node3(172.17.0.4)
            ........
            rpc_address: 172.17.0.2                         #Awalnya "localhost", diganti IP masing-masing node, node1(172.17.0.2), node2(172.17.0.3), node3(172.17.0.4)

## Menjalankan Cassandra :
          
             root# service cassandra start
             
             root# service cassandra status
               * Cassandra is running
               
             root# nodetoatus
             =======================
             Status=Up/Down
             |/ State=Normal/Leaving/Joining/Moving
              --  Address     Load       Tokens       Owns (effective)  Host ID                          Rack
             UN  172.17.0.3  221.11 KiB   256          ?       24ebee89-7779-4904-82d6-138244006375  rack1
             UN  172.17.0.2  449.22 KiB   256          ?       8efa9bcd-83ec-412c-a2dd-a736aacf6956  rack1
             UN  172.17.0.4  432.26 KiB   256          ?       ec854883-ab41-4f79-b176-b77679e713de  rack1


## Membuat Keyspace dengan nama "project", 
- Dilakukan sekali saja disembarang node. boleh node1, node2 atau node3
- Masuk pada cqlsh

      root# cqlsh 172.17.0.2
      
- Buat Kesypace :
      
      cqlsh> CREATE KEYSPACE project
      WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};
 
*Catatan
 replication_factor berjumlah 3 karna menyesuaikan node yang ada untuk melakukan replika dalam mendistribusikan data di dalam node  
 
    
## Membuat Tabel dengan nama "dokumen"
- Masuk Pada container "Cassandra-server1" dengan perintah
    
      # cqlsh 172.17.0.2
   
- Memilih keyspace

      cqlsh> USE project

- Buat tabel

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

 
## Membuat Tabel dengan nama "user_app"
    
    CREATE TABLE user_app (
    jabatan text,
    nip int,
    password text,
    username text,
    PRIMARY KEY (jabatan, nip))
    

## *Catatan
perintah pembuatan table hanya dilakukan satu kali saja pada server virtual, bisa dibuat disembarang server virtual bisa di node1, node2 atau node3.

## Sample Data
    # cqlsh 172.17.0.2
    
    cqlsh:project> use project

    cqlsh:project> INSERT INTO doc1 (nim , prodi , tahun , judul , kata_kunci , angkatan , intisari , nama_mhs , pembimbing , password , file1, file2, file3, file4, file5 ) VALUES ( 135410091, 'Teknik Informatika', 2017, 'Arsip Dokumen dengan Cassandra implementasi Multi Node Single Cluster ', 'rsip Dokumen dengan Cassandra implementasi Multi Node Single Cluster', '2013-01-01', 'rsip Dokumen dengan Cassandra implementasi Multi Node Single Cluster', 'Ahmad Anwar', 'Bambang PDP', 'aku', 'data', 'data', 'data', 'data', 'data');
    
    
    INSERT INTO dokumen(nim , prodi , tahun , judul , kata_kunci , angkatan , intisari , nama_mhs , pembimbing , password , file1, file2, file3, file4, file5 ) VALUES ( 135410121, 'Sistem Informasi', 2017, 'Big data untuk penjualan ', 'Big data', 2013, 'big data', 'Heru', 'Dr.Bambang PDP', 'aku', 'data', 'data', 'data', 'data', 'data');

    INSERT INTO dokumen (nim , prodi , tahun , judul , kata_kunci , angkatan , intisari , nama_mhs , pembimbing , password , file1, file2, file3, file4, file5 ) VALUES ( 135410100, 'Teknik Informatika', 2017, 'Coba pemodelan data 1', 'Coba pemodelan data 1',2013, 'Coba pemodelan data 1', 'Ibnu Masud', 'Dr.Bambang PDP', 'aku', 'data', 'data', 'data', 'data', 'data');
    
    INSERT INTO dokumen (nim , prodi , tahun , judul , kata_kunci , angkatan , intisari , nama_mhs , pembimbing , password , file1, file2, file3, file4, file5 ) VALUES ( 135410122, 'Teknik Informatika', 2017, 'Coba pemodelan data 2', 'Coba pemodelan data 2', 2013, 'Coba pemodelan data 2', 'Usam BIn Afan', 'Dr.Bambang PDP', 'aku', 'data', 'data', 'data', 'data', 'data');
    
    INSERT INTO dokumen (nim , prodi , tahun , judul , kata_kunci , angkatan , intisari , nama_mhs , pembimbing , password , file1, file2, file3, file4, file5 ) VALUES ( 135410333, 'Sistem Informasi', 2017, 'Coba pemodelan data 3', 'Coba pemodelan data 3', 2013, 'Coba pemodelan data 3', 'Abu Hamzah', 'Dr.Bambang PDP', 'aku', 'data', 'data', 'data', 'data', 'data');


## Membuat Index SASI
Ini diguanakan untuk mengimplementasikan menu pencarian pada table dokumen berdasarkan jundul, dengan ini query LIKE bisa aktif
       
    cqlsh:project> CREATE CUSTOM INDEX cari_judul ON project.dokumen ( judul ) USING 'org.apache.cassandra.index.sasi.SASIIndex' WITH OPTIONS = { 
    'analyzed' : 'true', 
    'analyzer_class' : 'org.apache.cassandra.index.sasi.analyzer.NonTokenizingAnalyzer', 
    'case_sensitive' : 'false', 
    'mode' : 'CONTAINS' 
    };


## Uji Coba mencari data dengan kata "cluster" pada tabel dokumen
    cqlsh:project> SELECT * FROM dokumen WHERE judul LIKE '%cluster%'


## Menjalankan Program
- Dilakukan di komputer host
- Instal semua keperluan untuk menjalankan framework Flask :-> Sample Ubuntu OS install flask 

      $ sudo apt-get install python-virtualenv

- Instal Driver Cassandra
       
      $  pip install cassandra-driver
      $  apt-get install libev4 libev-dev
      
- Pull aplikasi dan masuk pada folder
- Mengaktifkan environman aplikasi

      Web_Flask_Cassandra$ source flask/bin/activate
      
- Sampai terlihat ada "(flask)" didepan folder

      (flask) Web_Flask_Cassandra$ 

 - Instal CQLAlchemy
 
       (flask) Web_Flask_Cassandra$ pip install flask-cqlalchemy
 
-  ketik perintah
      
       (flask) Web_Flask_Cassandra$ python run.py
      
- Membuka browser ketik url
      
       127.0.0.1:5000
      



             
             
               

            
