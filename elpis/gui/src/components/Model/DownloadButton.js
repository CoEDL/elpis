import React, {useState} from "react";
import {Button, Loader, Segment} from "semantic-ui-react";
import urls from "urls";

export default function DownloadButton() {
  const [downloading, setDownloading] = useState(false);
  const download_model = async () => {
    setDownloading(true);
    await fetch(urls.api.model.download);
    setDownloading(false);
  };

  return (
      <Segment>
          <Button onClick={download_model}>Download Model</Button>
          {downloading && (
              <Loader indeterminate active>
                  {/* TODO Add size of file being downloaded */}
                  Zipping and Downloading Model. This may take a long time.
              </Loader>
      )}
      </Segment>
  );
}
