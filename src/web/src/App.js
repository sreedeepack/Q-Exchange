import React, {useEffect, useState} from 'react';
import './App.css';
import axios from 'axios';
import {Button, Card} from 'react-bootstrap';

function App() {

  const [submitted, setSubmitted] = useState(false);
  const [query, setQuery] = useState('');
  const [resultReturned, setResultReturned] = useState(true);
  const [num_results, setNum_results] = useState('10');
  const [searchresults, setSearchResults] = useState([]);
  const [tags, setTags] = useState([]);

  useEffect(() => {
    if(query.length > 0){
      setSubmitted(true)
      // try{

      //   axios.get('http://0.0.0.0:5000/search', {
      //     params: {
      //       "query": query,
      //       "num_results": num_results
      //     }
      //   })
      //   .then((response) => {
      //       setTags(response.data.tags[0])
      //       setSearchResults(response.data.results)
      //   });
      // }
      // catch(e){
      //   console.log('Error: ' + e)
      // }
    }
    else{
      setTimeout(() => {
        setSubmitted(false)
        setSearchResults([])
        setTags([])
      }, 700);

    }
  }, [query, num_results])

  const callAPI = () => {
    try{
      console.log("API Called")
      axios.get('http://0.0.0.0:5000/search', {
        params: {
          "query": query,
          "num_results": num_results
        }
      })
      .then((response) => {
          setTags(response.data.tags[0])
          setSearchResults(response.data.results)
      });
    }
    catch(e){
      console.log('Error: ' + e)
    }
  }

  var Tags = tags.map((tag,i) => {
    return (
        <Button className="tags" onClick={() => {
          var text = (query.valueOf() + " " + tag);
          setQuery(text);
        }}>{tag}</Button>
    );
  });

  const renderTags = () => {
    if(tags.length > 0){
      return(
        <div className="inputfieldcontainer">
          <h1 className="predicted_tags_h1">Suggested Tags</h1>
          {Tags}
        </div>
      );
    }
  }

  var renderResults = searchresults.map((result,i) => {
    return(
        <a target="_blank" className="searchresultlink" href={result.url}>
          <div className="searchresult">
            <div className="row">
              <div className="col-12 col-md-2">
                <h2 className="text-center">Votes</h2>
                <h3 className="text-center">{result.votes}</h3>
              </div>
              <div className="col-12 col-md-10">
                <h1>{result.title}</h1>
                <p dangerouslySetInnerHTML={{__html: result.body}}/>
              </div>
              <div className="col-12">
                <h4 style={{paddingLeft: "8px"}}>No. of answers: <span
                    style={{color: '#2F68B2', fontFamily: 'Axiforma Bold'}}>{(result.answers)}</span></h4>
              </div>
              <div className="col-12">
                <h4 style={{paddingLeft: "8px"}}>Date: <span
                    style={{color: '#2F68B2', fontFamily: 'Axiforma Bold'}}>{(result.date)}</span></h4>
              </div>
              <div className="col-12">
                <h4 style={{paddingLeft: "8px"}}>Similarity Score: <span
                    style={{color: '#2F68B2', fontFamily: 'Axiforma Bold'}}>{result.similarity_score}</span></h4>
              </div>
              <div className="col-12">
                <h4 style={{paddingLeft: "8px"}}><span
                    style={{
                      color: '#2F68B2',
                      fontFamily: 'Axiforma Bold'
                    }}>{result.src.replace('https:/', '').replace('.com/', '').replace('/', '')}</span></h4>
              </div>

            </div>
          </div>
        </a>
    );
  });

  return (
    <div>
      <div className="container">
        <Card className={submitted ? 'maincard' : 'inviscard'} style={{'margin-top': submitted ? '10%' : '30%'}}>
          <Card.Body>
            <div class="form-group has-feedback" className="inputfieldcontainer">
              <h1 className="num_results_h1"
                  style={{color: submitted ? '#464646' : 'white', fontSize: "25px"}}> Q-EXCHANGE </h1>

              <div class="input-group">
                <input id="query-box" type="text" className="form-control inputfield" value={query}
                       placeholder="Search Query"
                       style={{
                         borderBottomRightRadius: submitted ? '0px' : '10px',
                         borderTopRightRadius: submitted ? '0px' : '10px'
                       }}
                       onChange={(e) => setQuery(e.target.value)}/>
                <div class="input-group-append">
                  <Button className="inputfield tags" style={{'display': submitted ? 'block' : 'none'}}
                          onClick={callAPI} type="submit">Search</Button>
                </div>
              </div>

              {/*<input type="text" className="form-control inputfield" value={query} placeholder="Search Query"*/}
              {/*       onChange={(e) => setQuery(e.target.value)}/>*/}
              {/*<i className="fas fa-search search_icon"/>*/}

              <div className="row" style={{marginTop: '10px'}}>
                <div className="col-md-6">
                </div>
                <div className="col-12 col-md-6">
                  <div className="row">
                    <div className="col-9">
                      <h1 className="num_results_h1" style={{color: submitted ? '#464646' : 'white'}}>No. of results to
                        return: </h1>
                    </div>
                    <div className="col-2">

                    <input type="number" class="form-control inputfield inputfield2" value={num_results} onChange={(e) => setNum_results(e.target.value)}/>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {renderTags()}
            <br/><br/>
            {renderResults}
          </Card.Body>
        </Card>
        <br/>
      <br />
      </div>
    </div>
  );
}

export default App;
