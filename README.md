# validation_utils

This is the common utils for validate data and make manipulation with data.

Common usage is validate and easy maintain data flow.

Each time when you want create some view or handler for some data, you must do equal steps each time.
For example:
  ```
      schema = schema.loads(data)
      if not schema.is_valid():
        raise SomeException()

      validated_data = schema.validated_data
      process with validated data....
  ```
