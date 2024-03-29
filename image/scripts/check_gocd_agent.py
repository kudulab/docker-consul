import requests
import click

def get_agents(server_url, auth=None):
    with requests.Session() as s:
        if auth is not None:
            s.auth = auth
        server_url = server_url + '/go/api/agents'
        response = s.get(server_url, headers={'Accept': 'application/vnd.go.cd.v4+json'})
        if response.status_code != 200:
            raise RuntimeError('Failed to get agents from GoCD server')
        return response.json()['_embedded']['agents']

def check_agent_exists(all_agents, resource_name):
    for agent in all_agents:
        if resource_name in agent['resources'] and not ('Missing' == agent['agent_state'] or 'LostContact' == agent['agent_state']):
            return agent
    return None


@click.command()
@click.option('--go-server-url', help='URL to GoCD server')
@click.option('--go-agent-resource')
@click.option('--username')
@click.option('--password-file')
def check_agent(go_server_url, go_agent_resource, username, password_file):
    if username and password_file:
        with open(password_file, 'r') as content_file:
            content = content_file.read()
        auth = (username, content)
    else:
        auth = None
    agents = get_agents(go_server_url, auth)
    agent = check_agent_exists(agents, go_agent_resource)
    if agent:
        click.echo('Found agent: ' + agent['hostname'])
        exit(0)
    else:
        click.echo("Did not find agent with %s resource" % go_agent_resource)
        exit(2)


if __name__ == '__main__':
    check_agent()
