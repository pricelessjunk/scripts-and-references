fun main() {
  val first = listOf("personio", "chargebee-service")
  val second = listOf("employee_notes-cdc","attribute_updates-cdc")
  val third = listOf("employee_notes","attribute_updates")

  val result = mutableSetOf<String>()

  for(f in first) {
    for (s in second) {
      for (f2 in first) {
        for (t in third) {
          result.add("ebdr-stream-engine-pipe-cdc.$f.$s.$f2.$t.v1")
        }
      }
    }
  }

  println(result.size)
  println(result.joinToString(separator=","))
}
