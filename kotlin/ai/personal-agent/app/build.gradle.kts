plugins {
    kotlin("jvm") version "2.2.20"
    id("io.ktor.plugin") version "3.2.3"
    application
}

repositories {
    mavenCentral()
}

dependencies {

    implementation(kotlin("stdlib"))
    // implementation("com.openai:openai-java:3.5.2")
    implementation("io.ktor:ktor-server-core")
    implementation("io.ktor:ktor-server-netty")
    implementation("io.ktor:ktor-client-auth")
    implementation("io.modelcontextprotocol:kotlin-sdk:0.5.0")
//    implementation("org.slf4j:slf4j-simple:2.0.17")
//    implementation("ch.qos.logback:logback-classic:1.5.13")
    testImplementation(kotlin("test"))
}

//tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile> {
//    kotlinOptions {
//        jvmTarget = "1.8"
//    }
//}

 application {
     mainClass = "personal.agent.App"
 }

tasks.test {
    useJUnitPlatform()
}