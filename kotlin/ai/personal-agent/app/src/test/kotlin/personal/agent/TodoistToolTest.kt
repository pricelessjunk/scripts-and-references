package personal.agent

import kotlin.test.Test
import org.slf4j.LoggerFactory

class TodoistToolTest {
     private val logger = LoggerFactory.getLogger(javaClass)

    @Test
    fun todoistCheck() {
        val result = TodoistTool().getTodoistTasks()
        logger.info(result)
    }

}