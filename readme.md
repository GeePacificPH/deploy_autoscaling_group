# usage
- target: upload file/folder to AWS autoscaling group, using EC2 instance name tag and rsynch algorithm
- e.g:
    - name: Upload with rsynch \
      uses: ./ \
      with: \
        key_id: ${{secrets.KEY_ID}} \
        access_key: ${{secrets.ACCESS_KEY}} \
        region: 'valid AWS region name' \
        tag: ${{secrets.KEY_ID}} \
        port: '22' \
        user: ${{secrets.USER}} \
        pass: ${{secrets.PASS}} \
        key: ${{secrets.KEY}} \
        source: 'source file path' \
        target: 'target file path'