package com.example.mainapp.database;

import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoDatabase;
public class MongoDBClient {
    private static MongoClient mongoClient;
    private static MongoDatabase database;

    public static void initialize(){
        mongoClient = MongoClients.create("mongodb+srv://vuduyphuong:Phuong153280@vuduyphuong.odzmo8u.mongodb.net/");
        database = mongoClient.getDatabase("sensor");
    }

    public static MongoDatabase getDatabase(){
        if (database == null){
            initialize();
        }
        return database;
    }
}
