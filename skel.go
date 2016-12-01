package main

import (
	"github.com/urfave/cli"
	"os"
)

func main() {
	app := cli.NewApp()
	app.Name = "hello"
	app.Usage = "greet somebody"
	app.Action = func(c *cli.Context) {
		println("Hello,", c.Args()[0])
	}

	app.Run(os.Args)
}
