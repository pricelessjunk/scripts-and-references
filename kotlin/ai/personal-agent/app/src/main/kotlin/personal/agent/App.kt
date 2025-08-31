package personal.agent

class App {
    fun getGreeting(): String {
       return "Hello World!"
    }

    companion object {
        @JvmStatic
        fun main(args: Array<String>) {
            println(App().getGreeting())
        }
    }
}