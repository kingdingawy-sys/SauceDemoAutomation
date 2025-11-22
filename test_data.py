
users = [
    {
        "username": "standard_user",
        "password": "secret_sauce",
        "expected_behavior": "normal",
        "description": "Standard user with normal access"
    },
    {
        "username": "locked_out_user",
        "password": "secret_sauce",
        "expected_behavior": "locked_out",
        "description": "User account is locked out"
    },
    {
        "username": "problem_user",
        "password": "secret_sauce",
        "expected_behavior": "problematic_images",
        "description": "User sees broken images"
    },
    {
        "username": "performance_glitch_user",
        "password": "secret_sauce",
        "expected_behavior": "slow",
        "description": "User experiences slow performance"
    }
]