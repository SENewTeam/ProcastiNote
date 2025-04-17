/* eslint-disable react/prop-types */
import Button from "react-bootstrap/Button";
import Spinner from 'react-bootstrap/Spinner';
import { useState, forwardRef } from "react";
import { FeaturesApi } from "../utils/requests";
import '@toast-ui/editor/dist/toastui-editor.css';

import { Editor } from '@toast-ui/react-editor';

const AiRewrite = forwardRef(function AiRewrite({ comment, setComment }, ref) {
  const [buttonContent, setButtonContent] = useState("✨");

  return (
    <div style={{ position: "relative" }}>
      <Editor
        as="textarea"
        initialEditType="wysiwyg"
        initialValue={comment}
        onChange={() => {
          setComment(ref.current.getInstance().getMarkdown());
        }}
        ref={ref}
      />
      <Button
        variant="secondary"
        style={{ position: "absolute", right: "10px", bottom: "10px" }}
        onClick={() => {
          setButtonContent(<Spinner animation="grow" size="sm" />);
          FeaturesApi.aiRewrite(comment).then((res) => {
            setComment(res.rewritten_text);
            ref.current.getInstance().setMarkdown(res.rewritten_text);
            setButtonContent("✨");
          }).catch((err) => {
            console.log(err);
            setButtonContent("✨");
          });
        }}
      >
        {buttonContent}
      </Button>
    </div>
  );
});

export default AiRewrite;
