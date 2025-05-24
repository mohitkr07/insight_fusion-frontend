import os
from openai import OpenAI

client = OpenAI(
)

import json

class AgentGroup:
    def __init__(self):
        self.client = client
        self.conversation = []
        self.agents = {
            "classifier": "Error Classification Agent",
            "cluster_specialist": "Cluster Recovery Agent",
            "data_quality": "Data Quality Agent",
            "escalation": "Escalation Manager"
        }
    
    def _agent_message(self, agent_name, prompt, force_categories=None):
        """Generate agent response using OpenAI, optionally enforcing category classification."""
        
        if force_categories and agent_name == "classifier":
            categories_str = "\n- " + "\n- ".join(force_categories)
            prompt = f"""You must classify the following error into ONE of the predefined categories exactly as listed below:{categories_str}

    Do not make up new categories. Output ONLY the matching category and optionally a brief reason.
    Context:\n{prompt}"""

        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{
                "role": "system",
                "content": f"You are {self.agents[agent_name]}. Analyze the error and conversation history. Provide concise technical analysis."
            }, {
                "role": "user",
                "content": prompt
            }]
        )
        return response.choices[0].message.content


    def resolve_error(self, error_log):
        self.conversation = [{"role": "system", "content": f"New error received: {error_log}"}]
        
        max_rounds = 3
        resolution = None
        
        for _ in range(max_rounds):
            # Classification Agent starts

            categories = [
                "Cluster Unavailable/Terminated",
                "Job/Activity Dependency Failure",
                "Data Quality Expectation Failure",
                "Infrastructure/Library Error",
                "Unknown/Unclassified",
                "Process/Logic Errors"
            ]

            class_analysis = self._agent_message(
                "classifier", 
                f"{self._format_convo()}",
                force_categories=categories
            )
            
            self._add_to_convo("classifier", class_analysis)

            # Cluster Specialist response
            if "cluster" in class_analysis.lower():
                cluster_plan = self._agent_message("cluster_specialist",
                    f"Propose cluster recovery steps:\n{self._format_convo()}")
                self._add_to_convo("cluster_specialist", cluster_plan)
                
                if "restart" in cluster_plan:
                    # Execute actual cluster restart via API
                    cluster_id = self._extract_cluster_id(error_log)
                    success = self._restart_cluster(cluster_id)
                    
                    if success:
                        resolution = f"Cluster {cluster_id} restarted successfully"
                        break

            # Data Quality Agent
            if "data quality" in class_analysis.lower():
                dq_analysis = self._agent_message("data_quality",
                    f"Suggest data validation steps:\n{self._format_convo()}")
                self._add_to_convo("data_quality", dq_analysis)

            # Escalation check
            escalate_check = self._agent_message("escalation",
                f"Should we escalate? Consider:\n{self._format_convo()}")
            
            if "yes" in escalate_check.lower():
                self._escalate_to_human()
                resolution = "Escalated to human team"
                break

        return resolution, self.conversation

    def _restart_cluster(self, cluster_id):
        """Actual API call to restart cluster"""
        print(f"Restarting cluster {cluster_id}...")
        return True  # Simplified for example

    def _escalate_to_human(self):
        """Trigger escalation workflow"""
        print("Escalating to SRE team...")

    def _add_to_convo(self, agent, message):
        self.conversation.append({
            "role": self.agents[agent],
            "content": message,
            "agent": agent
        })

    def _format_convo(self):
        return "\n".join([f"{msg['role']}: {msg['content']}" 
                        for msg in self.conversation])
        
    def _extract_cluster_id(self, error_log):
        return 123456

# Usage
group = AgentGroup()
resolution, convo = group.resolve_error("Cluster terminated unexpectedly (ID: cluster-123)")
print(f"Final Resolution: {resolution}")
