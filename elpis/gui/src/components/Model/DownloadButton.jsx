import React, { useState } from "react";
import Button from "semantic-ui-react";
import urls from "urls";

export default function ModelButton() {
  const [downloading, setDownloading] = useState(false);

  const download_model = async () => {
    setDownloading(true);
    const response = await fetch(urls.api.model.download);
    setDownloading(false);
  };

  return (
    <div>
      <Button>Download Model</Button>
      {downloading && <p>This will take a long time.</p>}
    </div>
  );
}
