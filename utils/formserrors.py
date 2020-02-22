class FormsMixin():
    def get_errors(self):
       if hasattr(self,'errors'):
           error = self.errors.get_json_data()
           new_error = {}
           for key, message_lists in error.items():
               messages = []
               for message_dict in message_lists:
                   message = message_dict['message']
                   messages.append(message)
               new_error[key] = messages
           err = []
           for error in new_error.values():
               err.append(error)
           return err[-1]
       else:
           return {}
