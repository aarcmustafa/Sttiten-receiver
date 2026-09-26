package org.receiver.satellitecontroller

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainActivity : AppCompatActivity() {

    private lateinit var infoTextView: TextView
    private lateinit var sendButton: Button
    private lateinit var loadJsonButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val layout = android.widget.LinearLayout(this).apply {
            orientation = android.widget.LinearLayout.VERTICAL
            setPadding(50, 50, 50, 50)
        }

        infoTextView = TextView(this).apply {
            text = "تطبيق Stitten-receiver جاهز..."
            textSize = 15f
        }

        sendButton = Button(this).apply {
            text = "إرسال أمر للريسيفر"
            setOnClickListener {
                executeReceiverCommand()
            }
        }

        loadJsonButton = Button(this).apply {
            text = "قراءة إعدادات tcp.json"
            setOnClickListener {
                val content = ReceiverClient.loadJsonConfig(this@MainActivity, "tcp.json")
                infoTextView.text = if (content != null) "محتوى tcp.json:\n$content" else "فشل قراءة الملف"
            }
        }

        layout.addView(infoTextView)
        layout.addView(sendButton)
        layout.addView(loadJsonButton)
        setContentView(layout)
    }

    private fun executeReceiverCommand() {
        infoTextView.text = "جاري الاتصال..."
        CoroutineScope(Dispatchers.IO).launch {
            val response = ReceiverClient.sendCommand("19")
            val result = ReceiverClient.extractAndDecompress(response)

            withContext(Dispatchers.Main) {
                infoTextView.text = if (result != null) "النتيجة:\n$result" else "فشل الاتصال بالريسيفر"
            }
        }
    }
}
