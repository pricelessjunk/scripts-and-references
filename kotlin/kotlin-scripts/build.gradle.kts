import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
	kotlin("jvm") version "2.1.0"
	application
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

repositories {
	mavenCentral()
}

application {
	var mainClassName = findProperty("mainClass") as String?
	if (mainClassName == null) {
		mainClassName = "helloworld.HelloWorldKt"
	} 
	mainClass.set(mainClassName)
}

dependencies {
	implementation("org.apache.httpcomponents.client5:httpclient5:5.2.1")
	implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.12.1")
}

tasks.withType<KotlinCompile> {
	kotlinOptions {
		freeCompilerArgs += "-Xjsr305=strict"
		jvmTarget = "21"
	}
}

// tasks.withType<Test> {
// 	useJUnitPlatform()
// }
