name: Auto Update live.m3u

on:
  push:
    branches:
      - main
      - test-trigger
  schedule:
    - cron: '*/1 * * * *'  # 每分钟一次

jobs:
  update-file:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.x

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests

    - name: Run Python script
      run: |
        python extract_9901.py

    - name: Commit changes
      env:
        SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
      run: |
        mkdir -p ~/.ssh
        echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
        chmod 600 ~/.ssh/id_rsa
        ssh-keyscan github.com >> ~/.ssh/known_hosts
        git config --global user.name 'GitHub Action'
        git config --global user.email 'action@github.com'
        git add live.m3u
        git commit -m 'Update live.m3u with new 9901 port addresses'
        git push git@github.com:${{ github.repository }}.git HEAD:main
