package main

import (
	"encoding/csv"
	"fmt"
	"html/template"
	"io"
	"log"
	"os"
	"path"
	"sort"
	"strconv"
	"strings"
)

func try[T any](v T, err error) T {
	if err != nil {
		log.Fatal(err)
	}

	return v
}

func atoi(number string) int {
	result, err := strconv.Atoi(number)

	if err != nil {
		log.Fatal(err)
	}

	return result
}

func csvReadWithoutHeader[T any](path string, converter func([]string) T) []T {
	result := []T{}
	links := try(os.Open(path))

	defer links.Close()

	csvReader := csv.NewReader(links)

	_, err := csvReader.Read()
	if err == io.EOF {
		return result
	}
	if err != nil {
		log.Fatal(err)
	}

	for {
		record, err := csvReader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		result = append(result, converter(record))
	}

	return result
}

type Link struct {
	URL         string
	Title       string
	Description string
	Tags        []int
}

type TagAlias struct {
	Name string
	ID   int
}

type TagName struct {
	ID   int
	Name string
}

type Tags struct {
	IdToName      map[int]string
	NameToId      map[string]int
	IdToShortName map[int]string
}

type LinkTag struct {
	LinkID int
	TagID  int
}

type LinkTagMap map[int][]int

type OutputTag struct {
	ID   int
	Name string
}

type OutputLink struct {
	ID          int
	URL         string
	Title       string
	Description string
	LinkTags    []OutputTag
}

type TemplateState struct {
	OutputLinks []OutputLink
	OutputTags  []OutputTag
}

func csvToPartialLink(record []string) Link {
	url := record[0]
	title := record[1]
	description := record[2]

	return Link{url, title, description, []int{}}
}

func csvToTagAlias(record []string) TagAlias {
	tagMapper := record[0]
	tagID := atoi(record[1])

	return TagAlias{tagMapper, tagID}
}

func csvToTagName(record []string) TagName {
	tagID := atoi(record[0])
	tagName := record[1]

	return TagName{tagID, tagName}
}

func makeTags(names []TagName, aliases []TagAlias) Tags {
	idToName := map[int]string{}
	nameToId := map[string]int{}
	idToShortName := map[int]string{}

	for _, name := range names {
		idToName[name.ID] = name.Name
	}

	for _, alias := range aliases {
		nameToId[alias.Name] = alias.ID

		_, ok := idToShortName[alias.ID]
		if !ok {
			idToShortName[alias.ID] = alias.Name
		}
	}

	return Tags{idToName, nameToId, idToShortName}
}

func outputLinksDatabaseCSV(path string, links []Link, tags Tags) {
	output := try(os.Create(path))
	defer output.Close()

	fmt.Fprint(output, "url,title,description,tags\n")

	for _, link := range links {
		tagNames := []string{}

		for _, tagID := range link.Tags {
			tagNames = append(tagNames, tags.IdToShortName[tagID])
		}

		tagList := strings.Join(tagNames, ",")

		fmt.Fprintf(output, "\"%s\",\"%s\",\"%s\",\"%s\"\n", link.URL, link.Title, link.Description, tagList)
	}
}

func readLinksDatabaseCSV(path string, tags Tags) []Link {
	linkIndex := 0

	converter := func(record []string) Link {
		linkURL := record[0]
		linkTitle := record[1]
		linkDescription := record[2]
		linkTagNames := record[3]
		linkTags := []int{}

		linkIndex += 1

		tagNames := strings.Split(linkTagNames, ",")
		for _, tagName := range tagNames {
			tagID, ok := tags.NameToId[tagName]
			if ok {
				linkTags = append(linkTags, tagID)
			} else {
				log.Printf("Couldn't map tag name '%s' to a valid tag for link with ID=%d!\n", tagName, linkIndex+1)
			}
		}

		return Link{linkURL, linkTitle, linkDescription, linkTags}
	}

	return csvReadWithoutHeader(path, converter)
}

func initTemplateState(links []Link, tags Tags) TemplateState {
	outputLinks := []OutputLink{}
	outputTags := []OutputTag{}

	for key, value := range tags.IdToName {
		outputTags = append(outputTags, OutputTag{key, value})
	}

	sort.Slice(outputTags, func(i, j int) bool {
		return outputTags[i].Name < outputTags[j].Name
	})

	for id, link := range links {
		tagInfo := []OutputTag{}

		for _, tagID := range link.Tags {
			tagInfo = append(tagInfo, OutputTag{tagID, tags.IdToName[tagID]})
		}

		outputLinks = append(outputLinks, OutputLink{id + 1, link.URL, link.Title, link.Description, tagInfo})
	}

	return TemplateState{outputLinks, outputTags}
}

func renderTemplate(inputPath string, outputPath string, state TemplateState) {
	htmlOutput := try(os.Create(outputPath))
	defer htmlOutput.Close()

	t := try(template.New(path.Base(inputPath)).ParseFiles(inputPath))

	err := t.Execute(htmlOutput, state)
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	indexFilePath := "index.csv"
	tagAliases := csvReadWithoutHeader("tag_mapper.csv", csvToTagAlias)
	tagNames := csvReadWithoutHeader("tags.csv", csvToTagName)
	tags := makeTags(tagNames, tagAliases)
	links := readLinksDatabaseCSV(indexFilePath, tags)
	state := initTemplateState(links, tags)

	outputLinksDatabaseCSV(indexFilePath, links, tags)
	renderTemplate("index.tmpl", "index.html", state)
}
