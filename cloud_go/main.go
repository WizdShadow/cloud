package main

import (
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
)

var folder = []string{"text_file", "image", "video", "web", "exe", "other", "archive", "sound", "table"}

func create_folders(name string) {
	for _, v := range folder {
		os.MkdirAll("upload/"+name+"/"+v, os.ModePerm)
	}
}

func KafkaConsumer() {
	c, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": "localhost:9094",
		"group.id":          "test-group",
		"auto.offset.reset": "earliest",
	})

	if err != nil {
		panic(err)
	}

	c.SubscribeTopics([]string{"file", "^aRegex.*[Tt]opic"}, nil)
	for {
		msg, err := c.ReadMessage(-1)
		if err == nil {
			fmt.Printf("Message on %s: %s\n", msg.TopicPartition, string(msg.Value))
			create_folders(string(msg.Value))
		}
	}
}

func UploadHandler(w http.ResponseWriter, r *http.Request) {
	file, handler, err := r.FormFile("file")
	if err != nil {
		fmt.Fprintln(w, "Error retrieving file:", err)
		return
	}

	defer file.Close()

	f, _ := os.Create(handler.Filename)
	io.Copy(f, file)

	http.Redirect(w, r, "http://localhost:8000/profile", http.StatusSeeOther)
}

func main() {
	go KafkaConsumer()
	fmt.Println("Кафка запущена")
	http.HandleFunc("/upload", UploadHandler)
	http.ListenAndServe(":8081", nil)
	fmt.Println("Сервер запущен")
}
