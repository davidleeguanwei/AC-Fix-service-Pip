FROM python:3.7

MAINTAINER Lee, Kuan-Wei from SELab in Department of CSIE, NTU

# Install sonar-scanner
RUN mkdir /opt/scanner
RUN curl -LO https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.4.0.2170-linux.zip
RUN unzip -d /opt/scanner sonar-scanner-cli-4.4.0.2170-linux.zip
RUN rm sonar-scanner-cli-4.4.0.2170-linux.zip
ENV SCANNER_HOME /opt/scanner/sonar-scanner-4.4.0.2170-linux/bin
ENV PATH $SCANNER_HOME:$PATH

# Define working directory and install AC-Fix-Service-Pip dependency
RUN mkdir /opt/project
ADD . /opt/ac-fix
WORKDIR /opt/ac-fix
RUN pip3 install -r requirements.txt
CMD python3 main.py docker
