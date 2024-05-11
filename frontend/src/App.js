import React, { useState } from 'react';
import axios from 'axios';
import { Collapse, Table, Button, Input, message, Upload, Spin } from 'antd';
import { UploadOutlined, CopyOutlined } from '@ant-design/icons';


function App() {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [jpnModelResult, setJpnModelResult] = useState(null);
  const [engModelResult, setEngModelResult] = useState(null);
  const [biLangModelResult, setbiLangModelResult] = useState(null);
  const [rawJpnResult, setJpnRawResult] = useState('');
  const [rawEngResult, setEngRawResult] = useState('');
  const [biLangModelRawResult, setBiLangModelRawResult] = useState('');

  const props = {
    beforeUpload: (file) => {
      const isMP3 = file.type === 'audio/mpeg';
      const isWAV = file.type === 'audio/wav';
      if (!isMP3 && !isWAV) {
        message.error(`${file.name} is not a MP3 or WAV file`);
        return Upload.LIST_IGNORE;
      }
      setFile(file);
      return false;
    },
    onChange: (info) => {
      if (info.fileList.length > 0) {
        setFile(info.fileList[0].originFileObj);
      }
    },
    onRemove: () => {
      setFile(null);
    },
    maxCount: 1,
  };

  const onFileUpload = async () => {
    setIsUploading(true);

    const upload_url = 'http://localhost:5051/upload';
    const compare_url = 'http://localhost:5051/bi-lang';

    if (!file) {
      message.error('Please select a file');
      setIsUploading(false);
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("engine", "-a-general-input");

      const response1 = await axios.post(upload_url, formData);
      setJpnModelResult(response1.data);
      setJpnRawResult(JSON.stringify(response1.data, null, 2));

      const formData2 = new FormData();
      formData2.append("file", file);
      formData2.append("engine", "-a-general-en");

      const response2 = await axios.post(upload_url, formData2);
      setEngModelResult(response2.data);
      setEngRawResult(JSON.stringify(response2.data, null, 2));

      const formData3 = new FormData();
      formData3.append("result_data", JSON.stringify(response1.data));
      formData3.append("result_data2", JSON.stringify(response2.data));
      if (response1.data['results'][0]['confidence'] > 0.999) {
        setbiLangModelResult(response1.data);
        setBiLangModelRawResult('JPN model is really good confidence, so use it!');
      } else if (response2.data['results'][0]['confidence'] > 0.999) {
        setbiLangModelResult(response2.data);
        setBiLangModelRawResult('ENG model is really good confidence, so use it!');
      } else {
        const response3 = await axios.post(compare_url, formData3);
        setbiLangModelResult(response3.data);
        setBiLangModelRawResult(JSON.stringify(response3.data, null, 2));
      }
    } catch (error) {
      message.error('Failed to upload file');
    } finally {
      setIsUploading(false);
    }
  };


  const dataSource = (jpnModelResult && engModelResult && biLangModelResult) ? [
    {
      key: 'confidence',
      attribute: 'Confidence',
      'JPN-model': jpnModelResult['results'][0]['confidence'],
      'ENG-model': engModelResult['results'][0]['confidence'],
      'Bi-Lang-model': biLangModelResult['results'][0]['confidence'],
    },
    {
      key: 'text',
      attribute: 'Text',
      'JPN-model': jpnModelResult['text'],
      'ENG-model': engModelResult['text'],
      'Bi-Lang-model': biLangModelResult['text'],
    },
  ] : [];

  const columns = [
    {
      title: 'Attribute',
      dataIndex: 'attribute',
      key: 'attribute',
    },
    {
      title: 'JPN-model',
      dataIndex: 'JPN-model',
      key: 'JPN-model',
    },
    {
      title: 'ENG-model',
      dataIndex: 'ENG-model',
      key: 'ENG-model',
    },
    {
      title: 'Bi-Lang-model',
      dataIndex: 'Bi-Lang-model',
      key: 'Bi-Lang-model',
    },
  ];

  const copyToClipboard = () => {
    navigator.clipboard.writeText(rawJpnResult).then(() => {
      message.success("Copied to clipboard!");
    });
  };


  return (
    <div className="App">
      <h1>AmiVoice Hands On Demo</h1>
      <Upload {...props}>
        <Button icon={<UploadOutlined />} disabled={isUploading}>Select MP3 or WAV File</Button>
      </Upload>
      <Button onClick={onFileUpload} style={{ margin: '10px' }} disabled={isUploading}>Upload</Button> {isUploading ? <Spin size="large" /> : null}
      {jpnModelResult && (
        <div>
          <Table dataSource={dataSource} columns={columns} pagination={false} />
        </div>
      )}
      <Collapse>
        <Collapse.Panel header="Raw Jpn Result Data" key="1">
          <Input.TextArea value={rawJpnResult} readOnly />
          <Button onClick={copyToClipboard} icon={<CopyOutlined />} style={{ marginTop: '10px' }}>Copy JSON</Button>
        </Collapse.Panel>
      </Collapse>
      <Collapse>
        <Collapse.Panel header="Raw Eng Result Data" key="1">
          <Input.TextArea value={rawEngResult} readOnly />
          <Button onClick={copyToClipboard} icon={<CopyOutlined />} style={{ marginTop: '10px' }}>Copy JSON</Button>
        </Collapse.Panel>
      </Collapse>
      <Collapse>
        <Collapse.Panel header="Bi Lang Result" key="1">
          <Input.TextArea value={biLangModelRawResult} readOnly />
          <Button onClick={copyToClipboard} icon={<CopyOutlined />} style={{ marginTop: '10px' }}>Copy JSON</Button>
        </Collapse.Panel>
      </Collapse>
    </div>
  );
}

export default App;
