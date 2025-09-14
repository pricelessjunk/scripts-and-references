package personal.agent

import io.ktor.client.HttpClient
import io.ktor.client.engine.cio.CIO
import io.ktor.client.plugins.auth.Auth
import io.ktor.client.plugins.auth.providers.BearerTokens
import io.ktor.client.plugins.auth.providers.bearer
import io.ktor.client.request.get
import io.ktor.client.statement.bodyAsText
import io.ktor.http.URLProtocol
import io.ktor.http.path
import io.ktor.server.util.url
import io.modelcontextprotocol.kotlin.sdk.CallToolResult
import io.modelcontextprotocol.kotlin.sdk.TextContent
import io.modelcontextprotocol.kotlin.sdk.Tool
import io.modelcontextprotocol.kotlin.sdk.server.RegisteredTool
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.buildJsonObject

/**
 * https://medium.com/@nishantpardamwar/building-an-mcp-server-in-kotlin-a-step-by-step-guide-7ec96c7d9e00
 * https://github.com/modelcontextprotocol/kotlin-sdk/blob/main/samples/weather-stdio-server/src/main/kotlin/io/modelcontextprotocol/sample/server/McpWeatherServer.kt
 */
class TodoistTool {
    val httpClient = HttpClient(CIO) {
        install(Auth) {
            bearer {
                loadTokens {
                    BearerTokens(
                        "01a9d96dce8989866204631bca01a392c2c14511", null
                    )
                }
            }
        }
    }

    val todoistTool = RegisteredTool(
        Tool(
            name = "get-todoist-tasks", description = "Get Todoist tasks", inputSchema = Tool.Input(
                properties = buildJsonObject {
                    /*putJsonObject("category") {
                        put("sync_token", "*")
                        put("resource_types", "[\"all\"]")
                    }*/
                }, required = null
            )
        )
    ) { request ->
//        val category = request.arguments["category"]?.jsonPrimitive?.content ?: return@RegisteredTool CallToolResult(
//            content = listOf(TextContent("Required field 'category' is missing"))
//        )

        val result = getTodoistTasks()
        CallToolResult(content = listOf(TextContent(result)))
    }

    fun getTodoistTasks(): String {
        val url = url {
            protocol = URLProtocol.HTTPS
            host = "api.todoist.com"
            path("api", "v1", "tasks")
        }

        val result = runBlocking {
//            httpClient.post(url) {
//                setBody(buildJsonObject {
//                    put("sync_token", "*")
//                    put("resource_types", "[\"all\"]")
//                }.toString())
//            }.bodyAsText()
            httpClient.get(url).bodyAsText()
        }

        return result
    }
}