import json
import aoran


def lambda_handler(event, context): 
  if 'queryStringParameters' not in event:
    return { 'statusCode': 400, 'body': 'Unsupported event.' }
  if 'word' not in event['queryStringParameters']:
    return { 'statusCode': 400, 'body': '\'word\' parameter is required.' }
  word = event['queryStringParameters']['word']
  article = aoran.resolve_article_for(word, database_file='/tmp/cmudict')
  return {
    'statusCode': 200,
    'headers': {
      'Content-Type': 'application/json'
    },
    'body': json.dumps({
      'article': article
    })
  }
