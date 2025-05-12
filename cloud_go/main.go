package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"

	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
	"github.com/golang-jwt/jwt/v5"
)

var folder = []string{"text_file", "image", "video", "web", "exe", "other", "archive", "sound", "table"}

func get_jwt(token string) string {
	// Парсим токен с ключом "secret"
	tokens, err := jwt.Parse(token, func(t *jwt.Token) (interface{}, error) {
		return []byte("secret"), nil
	})

	if err != nil || tokens == nil {
		return "" // Возвращаем пустую строку при ошибке
	}

	// Проверяем валидность токена и тип claims
	claims, ok := tokens.Claims.(jwt.MapClaims)
	if !ok || !tokens.Valid {
		return ""
	}

	// Безопасное извлечение поля "username"
	username, ok := claims["username"].(string)
	if !ok {
		return "" // Если "username" нет или это не строка
	}

	return username
}

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
	cookie, err := r.Cookie("token")
	if err != nil {
		http.Redirect(w, r, "/register", http.StatusSeeOther)
		return
	}

	name := get_jwt(cookie.Value)

	file, handler, err := r.FormFile("file")

	if err != nil {
		fmt.Fprintln(w, "Error retrieving file:", err)
		return
	}

	defer file.Close()

	filepath := filepath.Join("upload", name, handler.Filename)
	f, err := os.Create(filepath)
	if err != nil {
		fmt.Fprintln(w, "Error creating file:", err)
		return
	}
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
