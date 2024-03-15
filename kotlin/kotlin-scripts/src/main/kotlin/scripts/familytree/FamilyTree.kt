package scripts.familytree

import java.io.File
import java.net.URI
import java.net.URLEncoder
import java.net.http.HttpClient
import java.net.http.HttpRequest
import java.net.http.HttpResponse

fun main() {

    val lineage = File("src/main/kotlin/general/familytree/lineage").readText().replace("..", "\t")
    val values = mapOf(
        "format" to "json",
        "operation" to "temp_view",
        "family" to URLEncoder.encode(lineage, "UTF-8"),
        "focus" to "Kaustuv",
        "show_middle" to "1"
    )

    val urlEncodedString = values.map { e -> "${e.key}=${e.value}" }.joinToString("&")
    println(urlEncodedString)

    val client = HttpClient.newBuilder().build();
    val request = HttpRequest.newBuilder()
        .uri(URI.create("http://api.familyecho.com/"))
        .header("Content-Type","application/x-www-form-urlencoded")
        .POST(HttpRequest.BodyPublishers.ofString(urlEncodedString))
        .build()
    val response = client.send(request, HttpResponse.BodyHandlers.ofString());

    val regex = "http.*(?=\")".toRegex()
    val matchResult = regex.find(response.body())?.value?.replace("\\", "")
    println(matchResult)
}