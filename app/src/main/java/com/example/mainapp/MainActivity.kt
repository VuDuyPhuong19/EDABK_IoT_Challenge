package com.example.mainapp

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.TextView
import com.example.mainapp.databinding.ActivityMainBinding
import kotlinx.android.synthetic.main.activity_main.AirConditioner
import kotlinx.android.synthetic.main.activity_main.device_1
import kotlinx.android.synthetic.main.activity_main.device_2
import kotlinx.android.synthetic.main.activity_main.device_3
import kotlinx.android.synthetic.main.activity_main.device_4
import kotlinx.android.synthetic.main.device_controller.view.deviceStatus
import kotlinx.android.synthetic.main.device_controller.view.device_name
import kotlinx.android.synthetic.main.device_controller.view.device_temperature

private lateinit var binding: ActivityMainBinding
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        deviceProccess()
    }
    private fun deviceProccess(){
        device_1.device_name.text = "Device 1"

        device_2.device_name.text = "Device 2"
        device_3.device_name.text = "Device 3"
        device_4.device_name.text = "Device 4"

        //update text
//        device_1.device_temperature.text = s + "°C";
        //Change device status
        device_1.deviceStatus.setImageDrawable(getDrawable(R.drawable.points_green))
    }

}