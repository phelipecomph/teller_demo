from typing import List
import pandas as pd

class LogAnalist:
    def __init__(self):
        pass

    def analyze_log(self, log_list:List[str]):
        splited_logs = []
        for log in log_list:
            splited_logs.append(self._log_split(log))
        #print(splited_logs)
        self.log_type_counts = {'INFO': 0, 'ERROR': 0, 'WARNING': 0}
        self.log_message_counts = {}
        self.log_error_counts = {}
        for log in splited_logs:
            # Count the number of each log type
            for key in self.log_type_counts.keys():
                if log['type'] == key:
                    self.log_type_counts[key] += 1
            
            # Count Agent Responses
            if log['type'] == 'INFO':
                if log['message'].find('Agent Response: ') != -1:
                    log_message = log['message'].replace('Agent Response: ', '')
                    if log_message in self.log_message_counts:
                        self.log_message_counts[log_message][0] += 1
                    else:
                        self.log_message_counts[log_message] = [1]
            
            # Count Error
            if log['type'] == 'ERROR':
                log_message = log['message']
                if log_message in self.log_error_counts:
                    self.log_error_counts[log_message][0] += 1
                else:
                    self.log_error_counts[log_message] = [1]
        
        self._print_ouput()

    def _print_ouput(self):
        print("Log Summary:")
        # Print the log type counts
        for key in self.log_type_counts.keys():
            print(f"- {key} messages: {self.log_type_counts[key]}")
        print()

        # Top 3 AI responses
        print("Top 3 AI Responses:")
        df_messages = pd.DataFrame(data = self.log_message_counts).T.sort_values(by = 0, ascending=False).reset_index().head(3)
        for index, row in df_messages.iterrows():
            print(f"{index+1}. {row['index']} ({row[0]} times)")
        print()

        # Top 3 Commom Errors
        print("Top 3 Commom Errors:")
        df_errors = pd.DataFrame(data = self.log_error_counts).T.sort_values(by = 0, ascending=False).reset_index().head(3)
        for index, row in df_errors.iterrows():
            print(f"{index+1}. {row['index']} ({row[0]} times)")

    def _log_split(self, log: str):
        log = '] '.join(log.split('] ')[1:])
        log_type, log = log.split(' - ')
        
        return {'type':log_type, 'message':log}

if __name__ == '__main__':
    logs = [
        """[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?" """,
        """[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?" """,
        """[2025-02-20 14:32:10] INFO - Agent Response: "Hello! How can I help you today?" """,
        """[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms""",
        """[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms""",
        """[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms""",
        """[2025-02-20 14:33:15] ERROR - Model Timeout after 5000ms""",
        """[2025-02-20 14:33:15] ERROR - API Connection Failure""",
        """[2025-02-20 14:33:15] ERROR - API Connection Failure""",
        """[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that." """,
        """[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that." """,
        """[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that." """,
        """[2025-02-20 14:34:02] INFO - Agent Response: "I'm sorry, I didn't understand that." """,
        """[2025-02-20 14:34:02] INFO - Machine Deployed """,
        """[2025-02-20 14:32:10] INFO - Agent Response: "Please provide more details. """,
        """[2025-02-20 14:32:10] INFO - Agent Response: "Please provide more details. """,
        """[2025-02-20 14:32:10] INFO - Agent Response: "Test test""",
        """[2025-02-20 14:33:15] ERROR - Test Error"""
    ]

    logger = LogAnalist()
    logger.analyze_log(logs)