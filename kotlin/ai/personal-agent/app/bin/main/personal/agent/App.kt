package personal.agent

import io.ktor.utils.io.streams.asInput
import io.modelcontextprotocol.kotlin.sdk.Implementation
import io.modelcontextprotocol.kotlin.sdk.ServerCapabilities
import io.modelcontextprotocol.kotlin.sdk.server.Server
import io.modelcontextprotocol.kotlin.sdk.server.ServerOptions
import io.modelcontextprotocol.kotlin.sdk.server.StdioServerTransport
import kotlinx.coroutines.Job
import kotlinx.coroutines.runBlocking
import kotlinx.io.asSink
import kotlinx.io.buffered

class App {

/*
    This way doesn't work. embeddedServer is possibly wrong and have to opt for websockets.

    fun runBasicServer() {
        embeddedServer(CIO, port = 8090) {
            mcp { return@mcp configureMcp() }
        }.start(wait = true)
    }
*/

    fun configureMcp(): Server {
        val server = Server(
            serverInfo = Implementation(
                name = "todoist-mcp-server", version = "0.0.1"
            ), options = ServerOptions(
                capabilities = ServerCapabilities(
                    tools = ServerCapabilities.Tools(listChanged = false)
                )
            )
        )

        server.addTools(
            listOf(TodoistTool().todoistTool),
        )

        return server
    }

    companion object {

        @JvmStatic
        fun main(args: Array<String>) {
            val server = App().configureMcp()
            val transport = StdioServerTransport(
                System.`in`.asInput(),
                System.out.asSink().buffered()
            )

            runBlocking {
                server.connect(transport)
                val done = Job()
                server.onClose {
                    done.complete()
                }
                done.join()
            }
        }
    }
}

