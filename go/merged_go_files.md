<!-- ../../../../pandaCapital/chat/alchemyapi-go/example_test.go -->
```go
package alchemyapi_test

import (
	"log"

	alchemyapi "github.com/jpadilla/alchemyapi-go"
)

//const ALCHEMY_API_KEY = "fWIc7bhtj5KBPsVu26WVaPUy8unfNITD"

func ExampleAlchemyAPI_GetTitle() {
	alchemyAPIKey := ALCHEMY_API_KEY
	alchemyClient := alchemyapi.New(alchemyAPIKey)
	url := "http://www.cnn.com/2009/CRIME/01/13/missing.pilot/index.html"

	titleResponse, err := alchemyClient.GetTitle(url, alchemyapi.GetTitleOptions{})

	if err != nil {
		log.Fatal(err)
	}

	log.Printf("%v\n", titleResponse.Title)
}

func ExampleAlchemyAPI_GetText() {
	alchemyAPIKey := ALCHEMY_API_KEY
	alchemyClient := alchemyapi.New(alchemyAPIKey)
	url := "http://www.cnn.com/2009/CRIME/01/13/missing.pilot/index.html"

	textResponse, err := alchemyClient.GetText(url, alchemyapi.GetTextOptions{})

	if err != nil {
		log.Fatal(err)
	}

	log.Printf("%v\n", textResponse.Text)
}

```

<!-- ../../../../pandaCapital/chat/alchemyapi-go/alchemyapi_test.go -->
```go
package alchemyapi_test

import (
	"testing"

	alchemyapi "github.com/jpadilla/alchemyapi-go"
)

const ALCHEMY_API_KEY = "fWIc7bhtj5KBPsVu26WVaPUy8unfNITD"

var (
	//alchemyAPIKey = os.Getenv("ALCHEMY_API_KEY")
	alchemyAPIKey = ALCHEMY_API_KEY
	testURL       = "http://www.cnn.com/2009/CRIME/01/13/missing.pilot/index.html"
)

func init() {
	if len(alchemyAPIKey) == 0 {
		panic("ALCHEMY_API_KEY environment variable is not set, but is needed to run tests!\n")
	}
}

func TestAlchemyAPI_GetTitle(t *testing.T) {
	alchemyClient := alchemyapi.New(alchemyAPIKey)

	titleResponse, err := alchemyClient.GetTitle(testURL, alchemyapi.GetTitleOptions{})

	if err != nil || titleResponse.Status == "ERROR" {
		t.Error(err)
	}
}

func TestAlchemyAPI_GetText(t *testing.T) {
	alchemyClient := alchemyapi.New(alchemyAPIKey)

	textResponse, err := alchemyClient.GetText(testURL, alchemyapi.GetTextOptions{})

	if err != nil || textResponse.Status == "ERROR" {
		t.Error(err)
	}
}

```

<!-- ../../../../pandaCapital/chat/alchemyapi-go/model.go -->
```go
package alchemyapi

// GetTextOptions is the set of parameters that can be used on the URLGetText endpoint.
// For more details see http://www.alchemyapi.com/api/text/urls.html#text.
type GetTextOptions struct {
	UseMetadata  int
	ExtractLinks int
}

// GetTextResponse is the resource representing response from URLGetText endpoint.
// For more details see http://www.alchemyapi.com/api/text/urls.html#text.
type GetTextResponse struct {
	Status string
	URL    string
	Text   string
}

// GetTitleOptions is the set of parameters that can be used on the URLGetTitle endpoint.
// For more details see http://www.alchemyapi.com/api/text/urls.html#title.
type GetTitleOptions struct {
	UseMetadata int
}

// GetTitleResponse is the resource representing response from URLGetTitle endpoint.
// For more details see http://www.alchemyapi.com/api/text/urls.html#title.
type GetTitleResponse struct {
	Status string
	URL    string
	Title  string
}

```

<!-- ../../../../pandaCapital/chat/alchemyapi-go/alchemyapi.go -->
```go
// Package alchemyapi provides the binding for AlchemyAPI.
package alchemyapi

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"strconv"
)

// alchemyAPI is the public AlchemyAPI URL for APIs.
const alchemyAPI = "http://access.alchemyapi.com"

// textExtractionAPI is the public AlchemyAPI URL for URLGetText.
const textExtractionAPI = alchemyAPI + "/calls/url/URLGetText"

// titleExtractionAPI is the public AlchemyAPI URL for URLGetTitle.
const titleExtractionAPI = alchemyAPI + "/calls/url/URLGetTitle"

// AlchemyAPI is used to invoke API calls.
type AlchemyAPI struct {
	apikey string
}

// New returns a new AlchemyAPI client.
func New(apikey string) *AlchemyAPI {
	return &AlchemyAPI{apikey}
}

// GetTitle returns the extracted title for a given URL.
func (client *AlchemyAPI) GetTitle(requestedURL string, options GetTitleOptions) (*GetTitleResponse, error) {
	addr := titleExtractionAPI + "?"

	params := url.Values{}
	params.Add("apikey", client.apikey)
	params.Add("url", requestedURL)
	params.Add("outputMode", "json")

	if options.UseMetadata > 0 {
		params.Add("useMetadata", strconv.Itoa(options.UseMetadata))
	}

	addr += params.Encode()

	// Make request
	resp, err := http.Get(addr)

	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()

	if resp.StatusCode >= 500 {
		body, _ := ioutil.ReadAll(resp.Body)
		return nil, fmt.Errorf("Got non 200 status code: %s %q", resp.Status, body)
	}

	// Read the JSON message from the body.
	response := &GetTitleResponse{}
	decoder := json.NewDecoder(resp.Body)

	if err := decoder.Decode(&response); err != nil {
		return nil, err
	}

	return response, nil
}

// GetText returns the extracted text for a given URL.
func (client *AlchemyAPI) GetText(requestedURL string, options GetTextOptions) (*GetTextResponse, error) {
	addr := textExtractionAPI + "?"

	params := url.Values{}
	params.Add("apikey", client.apikey)
	params.Add("url", requestedURL)
	params.Add("outputMode", "json")

	if options.UseMetadata > 0 {
		params.Add("useMetadata", strconv.Itoa(options.UseMetadata))
	}

	if options.ExtractLinks > 0 {
		params.Add("extractLinks", strconv.Itoa(options.ExtractLinks))
	}

	addr += params.Encode()

	// Make request
	resp, err := http.Get(addr)

	if err != nil {
		return nil, err
	}

	defer resp.Body.Close()

	if resp.StatusCode >= 500 {
		body, _ := ioutil.ReadAll(resp.Body)
		return nil, fmt.Errorf("Got non 200 status code: %s %q", resp.Status, body)
	}

	// Read the JSON message from the body.
	response := &GetTextResponse{}
	decoder := json.NewDecoder(resp.Body)

	if err := decoder.Decode(&response); err != nil {
		return nil, err
	}

	return response, nil
}

```

