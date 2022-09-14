import React, { useState } from "react";
import { Button, Loader, Segment } from "semantic-ui-react";
import urls from "urls";

export default function ModelButton() {
  const [downloading, setDownloading] = useState(false);

  const download_model = async () => {
    setDownloading(true);
    const response = await fetch(urls.api.model.download);
    setDownloading(false);
  };

  return (
    <Segment>
      <Button>Download Model</Button>
      {downloading && (
        <Loader indeterminate>
          Zipping and Downloading Model. This may take a long time.
        </Loader>
      )}
    </Segment>
  );
}
