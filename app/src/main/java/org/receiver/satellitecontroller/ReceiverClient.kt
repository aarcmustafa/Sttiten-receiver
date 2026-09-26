package org.receiver.satellitecontroller

import android.content.Context
import android.util.Log
import java.io.IOException
import java.io.InputStream
import java.io.OutputStream
import java.net.InetSocketAddress
import java.net.Socket
import java.util.zip.Inflater

object ReceiverClient {
    private const val TAG = "ReceiverClient"
    private const val IP = "192.168.1.2"
    private const val PORT = 20000

    // قراءة ملفات الـ JSON من مجلد assets
    fun loadJsonConfig(context: Context, fileName: String): String? {
        return try {
            val inputStream = context.assets.open(fileName)
            val size = inputStream.available()
            val buffer = ByteArray(size)
            inputStream.read(buffer)
            inputStream.close()
            String(buffer, Charsets.UTF_8)
        } catch (e: IOException) {
            Log.e(TAG, "[!] خطأ في قراءة ملف الـ JSON: ${e.message}")
            null
        }
    }

    fun sendCommand(commandStr: String): ByteArray? {
        var socket: Socket? = null
        return try {
            socket = Socket()
            socket.connect(InetSocketAddress(IP, PORT), 5000)

            val payload = "{\"request\":\"$commandStr\"}"
            val headerPrefix = "Start"
            val headerSuffix = "End"

            val lengthStr = String.format("%07d", payload.length)
            val wrappedData = "$headerPrefix$lengthStr$headerSuffix$payload"

            Log.d(TAG, "[*] جاري إرسال الأمر: $commandStr...")
            val outputStream: OutputStream = socket.getOutputStream()
            outputStream.write(wrappedData.toByteArray(Charsets.UTF_8))
            outputStream.flush()

            val inputStream: InputStream = socket.getInputStream()
            val buffer = ByteArray(4096)
            val bytesRead = inputStream.read(buffer)

            if (bytesRead != -1) {
                val response = buffer.copyOfRange(0, bytesRead)
                Log.d(TAG, "[*] تم استقبال الرد الخام بحجم: ${response.size} بايت")
                response
            } else {
                null
            }
        } catch (e: Exception) {
            Log.e(TAG, "[!] حدث خطأ أثناء الاتصال: ${e.message}")
            null
        } finally {
            try {
                socket?.close()
            } catch (e: Exception) {}
        }
    }

    fun extractAndDecompress(responseBytes: ByteArray?): String? {
        if (responseBytes == null || responseBytes.isEmpty()) return null

        try {
            val zlibHeader = byteArrayOf(0x78.toByte(), 0x9C.toByte())
            var zlibIndex = -1

            for (i in 0..responseBytes.size - zlibHeader.size) {
                if (responseBytes[i] == zlibHeader[0] && responseBytes[i + 1] == zlibHeader[1]) {
                    zlibIndex = i
                    break
                }
            }

            if (zlibIndex != -1) {
                val compressedBytes = responseBytes.copyOfRange(zlibIndex, responseBytes.size)
                val inflater = Inflater()
                inflater.setInput(compressedBytes)
                val resultBuffer = ByteArray(65536)
                val resultLength = inflater.inflate(resultBuffer)
                inflater.end()

                return String(resultBuffer, 0, resultLength, Charsets.UTF_8)
            } else {
                return String(responseBytes, Charsets.UTF_8)
            }
        } catch (e: Exception) {
            Log.e(TAG, "[!] خطأ أثناء فك الضغط: ${e.message}")
            return null
        }
    }
}
