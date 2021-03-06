import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

buildscript {
	dependencies {
		classpath("com.h2database:h2:1.4.197")
	}
}

plugins {
	id("org.flywaydb.flyway") version "8.0.5"
	kotlin("jvm") version "1.5.21"
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("mysql:mysql-connector-java:8.0.12")
}


 // for use with a local sql instance.
flyway {
	url = "jdbc:mysql://${System.getenv("DEV_DB_HOST")}:3306/Token?useSSL=false" // for local
  //url = "jdbc:mysql://${System.getenv("DATA_DB_URL")}:3306/data?useSSL=false" // for cloud
    user = System.getenv("DEV_DB_USERNAME")
    password = System.getenv("DEV_DB_PASSWORD")
	baselineOnMigrate = true
	schemas = arrayOf("Token")
	locations = arrayOf("filesystem:${project.projectDir}/token/migrations")
} 