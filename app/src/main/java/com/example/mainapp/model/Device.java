package com.example.mainapp.model;

import com.google.gson.annotations.SerializedName;
public class Device {
    @SerializedName("temperature")
    private double temperature;
    @SerializedName("humidity")
    private double humidity;
    @SerializedName("device_on")
    private int device_on;
    @SerializedName("light_on")
    private int light_on;
    @SerializedName("air_conditioning_on")
    private int air_conditioning_on;
    @SerializedName("fan_on")
    private int fan_on;
    @SerializedName("tv_on")
    private int tv_on;
    @SerializedName("light1_state")
    private boolean light1_state;
    @SerializedName("light2_state")
    private boolean light2_state;
    @SerializedName("air_conditioning_state")
    private boolean air_conditioning_state;
    @SerializedName("fan_state")
    private boolean fan_state;
    @SerializedName("tv_state")
    private boolean tv_state;
    @SerializedName("time")
    private String time;

    // temperature Getter and Setter
    public double getTemperature(){
        return temperature;
    }
    public void setTemperature(double temperature){
        this.temperature = temperature;
    }
    // humidity Getter and Setter
    public double getHumidity(){
        return humidity;
    }
    public void setHumidity(double humidity){
        this.humidity = humidity;
    }
    // device_on Getter and Setter
    public int getDeviceOn(){
        return device_on;
    }
    public void setDeviceOn(int device_on){
        this.device_on = device_on;
    }
    // light_on Getter and Setter
    public int getLightOn(){
        return light_on;
    }
    public void setLightOn(int light_on){
        this.light_on = light_on;
    }
    // air_conditioning_on Getter and Setter
    public int getAirConditioningOn(){
        return air_conditioning_on;
    }
    public void setAirConditioningOn(int air_conditioning_on){
        this.air_conditioning_on = air_conditioning_on;
    }
    // fan_on Getter and Setter
    public int getFanOn(){
        return fan_on;
    }
    public void setFanOn(int fan_on){
        this.fan_on = fan_on;
    }
    // light_on Getter and Setter
    public int getTvOn(){
        return tv_on;
    }
    public void setTvOn(int tv_on){
        this.tv_on = tv_on;
    }
    // air_conditioning Getter and Setter
    public boolean getAirConditioningState(){
        return air_conditioning_state;
    }
    public void setAirConditioningState(boolean air_conditioning_state){ this.air_conditioning_state = air_conditioning_state; }
    // light1_state Getter and Setter
    public boolean getLight1State(){
        return light1_state;
    }
    public void setLight1State(boolean light1_state){
        this.light1_state = light1_state;
    }
    // light2_state Getter and Setter
    public boolean getLight2State(){
        return light2_state;
    }
    public void setLight2State(boolean light2_state){
        this.light2_state = light2_state;
    }
    // fan_state Getter and Setter
    public boolean getFanState(){
        return fan_state;
    }
    public void setFanState(boolean fan_state){
        this.fan_state = fan_state;
    }
    // tv_state Getter and Setter
    public boolean getTvState(){
        return tv_state;
    }
    public void setTvState(boolean tv_state){
        this.tv_state = tv_state;
    }
    // time Getter and Setter
    public String getTime(){
        return time;
    }
    public void setTime(String time) {
        this.time = time;
    }
}
