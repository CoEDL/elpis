import React, {useState} from "react";
import {Button, Loader, Segment} from "semantic-ui-react";
import urls from "urls";
import downloadjs from "downloadjs";

export default function DownloadButton() {
  const [downloading, setDownloading] = useState(false);
  const download_model = async () => {
    setDownloading(true);

    let response = await fetch(urls.api.model.download);
    let blob = await response.blob();

    downloadjs(blob, "model.zip", "application/zip");
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
