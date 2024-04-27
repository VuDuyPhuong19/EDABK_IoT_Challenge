package com.example.mainapp.database;

import android.os.Build;

import androidx.annotation.RequiresApi;

import com.example.mainapp.model.Device;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.changestream.ChangeStreamDocument;
import org.bson.Document;
public class DeviceRepository {
    private MongoCollection<Document> collection;

    // Constructor
    public DeviceRepository(){
        MongoDatabase db = MongoDBClient.getDatabase();
        collection = db.getCollection("sensor");
    }
    // Constructor with parameter
    public DeviceRepository(MongoDatabase db){
        collection = db.getCollection("sensor");
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    public void watchChanges(){
        collection.watch().forEach((ChangeStreamDocument<Document> change) -> {
            if (change.getOperationType().equals("insert")){
                Document newDoc = change.getFullDocument();
                System.out.println("New document inserted: " + newDoc.toJson());
                handleNewDeviceData(newDoc);
            }
        });
    }

    public Device handleNewDeviceData(Document document){
        Device device = new Device();
        device.setLightOn(document.getInteger("light_on", 0));
        device.setFanOn(document.getInteger("fan_on", 0));
        device.setTime(document.getString("time"));
        return device;
    }

    public Device getLatestDeviceData(){
        Document doc = collection.find().sort(new Document("time", -1)).first();
        if (doc != null){
            return handleNewDeviceData(doc);
        }
        return null;
    }
}
