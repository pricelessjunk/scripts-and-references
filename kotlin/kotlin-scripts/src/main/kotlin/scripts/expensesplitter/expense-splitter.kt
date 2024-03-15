package scripts.expensesplitter

import java.io.File

fun main(args: Array<String>) {
    val lines = readFileAsLinesUsingUseLines(args[0])

    var progress = 0
    var count = 0
    var arr: Array<DoubleArray>? = null
    val names = mutableListOf<String>()
    var totalSpend : DoubleArray? = null
    var nameCount = 0


    for (line in lines) {
        if (!line.startsWith('#') && line.isNotEmpty()) {
            if (progress == 0) {
                count = line.toInt()
                arr = Array(count) { DoubleArray(count) }
                totalSpend = DoubleArray(count)
                progress++
            } else if (progress == 1) {
                names.add(line)
                nameCount++

                if (nameCount == count) {
                    progress++
                }
            } else if (progress == 2) {
                processLine(arr!!, line, count, totalSpend!!)
            }
        }
    }

    printExpenses(arr!!, names, count, totalSpend!!)

}

fun readFileAsLinesUsingUseLines(fileName: String): List<String> = File(fileName).useLines { it.toList() }

fun processLine(arr: Array<DoubleArray>, line: String, count: Int, totalSpend: DoubleArray) {
    val splits = line.split(' ')
    var amount: Double = splits[0].toDouble()
    val payer: Int = splits[1].toInt() - 1
    totalSpend[payer] += amount

    when (val payee: String = splits[2]) {
        "even" -> {
            amount /= count

            for(i in 0 until count) {
                if(payer != i) {
                    arr[payer][i] += amount
                }
            }
        }
        "uneven" -> {
            val unevenPayees = splits[3].split(',').map { it.toInt() - 1 }.toIntArray()
            val unevenAmount = splits[4].split(',').map { it.toDouble() }.toDoubleArray()

            checkWarnings(unevenAmount, unevenPayees, amount)

            for(i in unevenPayees.indices) {
                if(unevenPayees[i] != payer) {
                    arr[payer][unevenPayees[i]] += unevenAmount[i]
                }
            }
        }
        else -> {
            val payeeList = payee.split(',').map { it.toInt() - 1 }.toList()
            amount /= payeeList.size

            for(i in payeeList) {
                arr[payer][i] += amount
            }
        }
    }
}

fun checkWarnings(unevenAmount: DoubleArray, unevenPayees: IntArray, amount: Double) {
    if(unevenPayees.size != unevenAmount.size) {
        println("WARNING: The size of the payees and amounts for uneven transaction does not match")
    }

    if(unevenAmount.sum() != amount) {
        println("WARNING: The total of all the amounts don't match up to $amount")
    }
}

fun printExpenses(arr: Array<DoubleArray>, names: List<String>, count: Int, totalSpend: DoubleArray) {
    arr.forEach {
        it.forEach { it2 -> print("${"%.2f".format(it2).toDouble()}\t\t\t") }
        println("\n")
    }

    for(i in 0 until count) {
        println("${names[i]} Total spend: ${totalSpend[i]}")
        println("${names[i]} Paid for self (excluding even, uneven payments): ${arr[i][i]}")

        for(j in 0 until count) {
            if (i != j) {
                if (arr[i][j] > arr[j][i]) {
                    val value = "%.2f".format(arr[i][j]-arr[j][i]).toDouble()
                    println("${names[j]} owes ${names[i]}: $value Euro")
                } else if(arr[j][i] > arr[i][j]) {
                    val value = "%.2f".format(arr[j][i]-arr[i][j]).toDouble()
                    println("${names[i]} owes ${names[j]}: $value Euro")
                }
            }
        }

        println()
    }
}