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

    private lateinit var statusTextView: TextView
    private lateinit var sendButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val layout = android.widget.LinearLayout(this).apply {
            orientation = android.widget.LinearLayout.VERTICAL
            setPadding(50, 50, 50, 50)
        }

        statusTextView = TextView(this).apply {
            text = "جاهز للاتصال بالريسيفر..."
            textSize = 16f
        }

        sendButton = Button(this).apply {
            text = "إرسال الأمر للريسيفر"
            setOnClickListener {
                executeReceiverCommand()
            }
        }

        layout.addView(statusTextView)
        layout.addView(sendButton)
        setContentView(layout)
    }

    private fun executeReceiverCommand() {
        statusTextView.text = "جاري إرسال الأمر..."

        CoroutineScope(Dispatchers.IO).launch {
            val response = ReceiverClient.sendCommand("19")
            val resultText = ReceiverClient.extractAndDecompress(response)

            withContext(Dispatchers.Main) {
                if (resultText != null) {
                    statusTextView.text = "النتيجة:\n$resultText"
                } else {
                    statusTextView.text = "فشل الاتصال أو الاستجابة فارغة."
                }
            }
        }
    }
}
